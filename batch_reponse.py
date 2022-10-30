import pandas as pd
import numpy as np




class BatchResponse:
    def __init__(self, id, bench_type, metric, batch_unit, batch_id, batch_size,analysis_parameter):
        self.id = id
        self.bench_type = bench_type
        self.metric = metric
        self.batch_id = int(batch_id)
        self.batch_size = int(batch_size)
        self.batch_unit = int(batch_unit)
        self.analysis_parameter=analysis_parameter
        self.csv_data = pd.read_csv("https://raw.githubusercontent.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems/master/Workload%20Data/" + bench_type + ".csv")



    # def convert_series_to_dict(self, batches):
    #     batch_list = list()
    #     for batch in batches:
    #         dict_batch = batch
    #         batch_list.append(dict_batch)
    #     return batch_list

    def create_batches(self):
        batches = list()
        column = self._get_column_from_csv()
        last_batch_id = self.batch_id
        for index in range(0, self.batch_size):
            batch = column[last_batch_id * self.batch_unit: (last_batch_id + 1) * self.batch_unit].to_dict()
            batches.append(batch)
            last_batch_id += 1

        return batches, (last_batch_id - 1)

    def data_analysis(self,pict_1):
        
        result={}
        for d in pict_1:
            result.update(d)

        v=list(result.values())
        arr=np.array(v)
        if self.analysis_parameter =='10p':
           percenta=np.percentile(arr,10) 
              
        elif self.analysis_parameter =='50p':
           percenta=np.percentile(arr,50) 
           
        elif self.analysis_parameter =='95p':
           percenta=np.percentile(arr,95) 
           
        elif self.analysis_parameter =='99p':
           percenta=np.percentile(arr,99) 
           
        elif self.analysis_parameter == 'avg':
            percenta=np.average(arr)
            
        elif self.analysis_parameter == 'std':
            percenta=np.std(arr)
            
        elif self.analysis_parameter == 'min':
            percenta=np.min(arr)
            
        elif self.analysis_parameter == 'max':
            percenta=np.max(arr)
            
        return percenta
        


    def binary_result(self):
        samples = self._number_of_samples()
        (batches, last_batch_id) = self.create_batches()
        
        
        data= self.data_analysis(batches)
        return {
            "rfw_id": self.id,
            "last_batch_id": last_batch_id,
            "number_of_samples": samples,
            "batches": batches,
            "analysis": data
        }

    # private methods

    def _get_column_from_csv(self):
        data_column = self.csv_data[self.metric]
        return data_column

    def _number_of_samples(self):
        return self.batch_size * self.batch_unit
