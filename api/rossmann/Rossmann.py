import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime



class Rossmann( object ):

    def __init__( self ):
        self.home_path = '/home/gustavo/repos/comunidade_ds/ds_em_producao/rossmann_project/'
        
        self.competition_distance_scaler   = pickle.load(open(self.home_path + 
                                                              'parameters/competition_distance_scaler.pkl', 'rb'))
        
        self.competition_time_month_scaler = pickle.load(open(self.home_path + 
                                                              'parameters/competition_time_month_scaler.pkl','rb'))
        
        self.promo_time_week_scaler        = pickle.load(open(self.home_path + 
                                                             'parameters/promo_time_week_scaler.pkl', 'rb'))
        
        self.year_scaler                   = pickle.load(open(self.home_path + 
                                                              'parameters/year_scaler.pkl', 'rb'))
        
        self.story_type_scaler             = pickle.load(open(self.home_path + 
                                                              'parameters/store_type_scaler.pkl', 'rb'))



    def data_cleaning( self, df1 ):

        ## 1.1 Rename Columns
        cols_old = df1.columns
        
        try:
            cols_old.remove('Sales')        # dados que queremos prever
            cols_old.remove('Customers')    # valor não conhecido no ambiente de produção
            
        except:
            pass

        snake_case = lambda x: inflection.underscore(x)

        cols_new = list( map(snake_case, cols_old) )

        df1.columns = cols_new



        ## 1.3 Data Type
        df1['date'] = pd.to_datetime(df1['date'])



        ## 1.5 Fillout NA

        # competition_distance
        df1['competition_distance'] = df1['competition_distance'].apply(lambda x: 200_000 if math.isnan(x) else x)

        # competition_open_since_month
        df1['competition_open_since_month'] = ( df1.apply(
                                                            lambda x: x['date'].month 
                                                            if math.isnan(x['competition_open_since_month']) 
                                                            else x['competition_open_since_month'], 
                                                    axis=1 )                                               )

        # competition_open_since_year
        df1['competition_open_since_year'] = ( df1.apply( 
                                                            lambda x: x['date'].year 
                                                            if math.isnan(x['competition_open_since_year']) 
                                                            else x['competition_open_since_year'], 
                                                    axis=1 ) 
                                             )
        
        # promo2_since_week
        df1['promo2_since_week'] = ( df1.apply(
                                                 lambda x: x['date'].week 
                                                 if math.isnan(x['promo2_since_week']) 
                                                 else x['promo2_since_week'], 
                                         axis=1 ) 
                                   )

        # promo2_since_year
        df1['promo2_since_year'] = ( df1.apply(
                                                 lambda x: x['date'].year 
                                                 if math.isnan(x['promo2_since_year']) 
                                                 else x['promo2_since_year'], 
                                         axis=1 ) 
                                   )

        # promo_interval
        month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 
                     9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        df1['promo_interval'].fillna( 0, inplace=True )

        df1['month_map'] = df1['date'].dt.month.map( month_map )

        df1['is_promo'] = ( df1[['promo_interval', 'month_map']]
                               .apply( lambda x: 0 if x['promo_interval'] == 0 else 
                                                 1 if x['month_map'] in x['promo_interval'].split(',') 
                                                   else 0, 
                                axis=1 ) 
                          )



        ## 1.6 Change Types

        # competition
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(int)
        df1['competition_open_since_year']  = df1['competition_open_since_year'].astype(int)

        # promo2
        df1['promo2_since_week'] = df1['promo2_since_week'].astype(int)
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(int)


        return df1



    def feature_engineering( self, df2 ):

        # year
        df2['year'] = df2['date'].dt.year

        # month
        df2['month'] = df2['date'].dt.month

        # day
        df2['day'] = df2['date'].dt.day

        # week of year
        df2['week_of_year'] = df2['date'].dt.weekofyear

        # year week
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')


        # competition_since / competition_time_month
        df2['competition_since'] = ( df2.apply( 
                                        lambda x: datetime.datetime( 
                                                                     year = x['competition_open_since_year'], 
                                                                     month = x['competition_open_since_month'], 
                                                                     day = 1 
                                                                ), 
                                        axis=1 ) 
                                   )

        df2['competition_time_month'] = ( ( df2['date'] - df2['competition_since'] ) / 30 ).dt.days


        # promo_since
        df2['promo_since'] = df2['promo2_since_year'].astype(str) + '-' + df2['promo2_since_week'].astype(str)
        df2['promo_since'] = ( df2['promo_since']
                                         .apply( 
                                                 lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - 
                                                           datetime.timedelta(days=7) 
                                            ) 
                                )
                                
        df2['promo_time_week'] = ( (df2['date'] - df2['promo_since']) / 7 ).dt.days


        # assortment
        assortment_map = {'a': 'basic', 'b': 'extra', 'c': 'extended'}
        df2['assortment'] = df2['assortment'].map( assortment_map )

        # state_holiday
        holiday_map = {'a': 'public_holiday', 'b': 'easter_holiday', 'c': 'christmas', '0': 'regular_day'}
        df2['state_holiday'] = df2['state_holiday'].map( holiday_map )


        

        # 3.0 Filtragem de Variáveis

        ## 3.1 Filtragem das Linhas
        df2 = df2[ df2['open'] != 0 ]

        ## 3.2 Seleção das Colunas
        cols_drop = ['open', 'promo_interval', 'month_map']

        df2 = df2.drop( cols_drop, axis=1 )


        return df2


    def data_preparation( self, df5 ):

        ## 5.2 Rescaling

        # competition_distance
        df5['competition_distance'] = ( self.competition_distance_scaler
                                            .transform( df5[['competition_distance']].values ) )
        # competition_time_month
        df5['competition_time_month'] = ( self.competition_time_month_scaler
                                              .transform( df5[['competition_time_month']].values ) )

        # promo_time_week
        df5['promo_time_week'] = self.promo_time_week_scaler.transform( df5[['promo_time_week']].values )

        # year
        df5['year'] = self.year_scaler.transform( df5[['year']].values )



        ### 5.3.1 Encoding

        # state_holiday - OneHotEncoding
        df5 = pd.get_dummies( df5, prefix=['state_holiday'], columns=['state_holiday'] )

        # store_type - LabelEncoding
        df5['store_type'] = self.story_type_scaler.transform( df5['store_type'] )

        # assortment - OrdinalEncoding
        assortment_dict = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map( assortment_dict )


        
        ### 5.3.2 Nature Transformation

        # month
        df5['month_sin'] = df5['month'].apply( lambda x: np.sin( x * (np.pi/12) ) )
        df5['month_cos'] = df5['month'].apply( lambda x: np.cos( x * (np.pi/12) ) )

        # day_of_week
        df5['day_of_week_sin'] = df5['day_of_week'].apply( lambda x: np.sin( x * (np.pi/7) ) )
        df5['day_of_week_cos'] = df5['day_of_week'].apply( lambda x: np.cos( x * (np.pi/7) ) )

        # day
        df5['day_sin'] = df5['day'].apply( lambda x: np.sin( x * (np.pi/30) ) )
        df5['day_cos'] = df5['day'].apply( lambda x: np.cos( x * (np.pi/30) ) )

        # week_of_year
        df5['week_of_year_sin'] = df5['week_of_year'].apply( lambda x: np.sin( x * (np.pi/52) ) )
        df5['week_of_year_cos'] = df5['week_of_year'].apply( lambda x: np.cos( x * (np.pi/52) ) )


        cols_selected = ['store', 'promo', 'store_type', 'assortment', 'competition_distance', 
                         'competition_open_since_month', 'competition_open_since_year',
                         'promo2', 'promo2_since_week', 'promo2_since_year', 'competition_time_month', 
                         'promo_time_week', 'day_of_week_sin', 'day_of_week_cos','month_sin', 'month_cos', 
                         'day_sin', 'day_cos', 'week_of_year_sin', 'week_of_year_cos']

        
        return df5[ cols_selected ]
    
    
    
    def get_prediction( self, model, original_data, test_data ):
        
        # prediction
        pred = model.predict( test_data )
        
        # join the prediction into the original data
        original_data['prediction'] = np.expm1( pred )
        
        
        return original_data.to_json( orient='records', date_format='iso' )
        




