import buf_pb2
import requests


batch_request = buf_pb2.Request()

id = input('Please Enter Request For Workload (RFW) ID:')
bench_type = input('Please type one of the following:\n 1. DVD-testing\n 2. DVD-training\n 3. NDBench-training\n'
                   '4. NDBench-training\n')
metric = input('Please type one of the metrics from the following:\n'
               '1. CPUUtilization_Average\n 2. NetworkIn_Average\n 3. NetworkOut_Average\n'
               ' 4. MemoryUtilization_Average\n')
batch_id = int(input('Please Enter the Batch Id (from which batch you want the data to start from) in integer: '))
batch_unit = int(input('Please Enter the number of samples you want in one batch in integer: '))
batch_size = int(input('Please Enter the number of batches to be returned in integer: '))
analysis_parameter = input('Enter the analysis you want : \n''1. 10p\n''2. 50p \n''3. 95p\n' '4. 99p\n''4. avg\n''5. std \n''6. max\n''7. min\n ')

batch_request.id = id
batch_request.bench_type = bench_type
batch_request.metric = metric
batch_request.batch_id = batch_id
batch_request.batch_unit = batch_unit
batch_request.batch_size = batch_size
batch_request.analysis_parameter=analysis_parameter

# batch_request.id = '123'
# batch_request.bench_type = 'DVD-testing'
# batch_request.metric = 'CPUUtilization_Average'
# batch_request.batch_id = 2
# batch_request.batch_unit = 2
# batch_request.batch_size = 2
# batch_request.analysis_parameter='avg'




res = requests.get("http://127.0.0.1:5000/get_batches?", headers={'Content-Type': 'application/protobuf'},
                   data=batch_request.SerializeToString())

print('sent')
print(res.content)
batch_response = buf_pb2.Response.FromString(res.content)
with open("proto_data.txt", "w") as file:
    file.write(str(batch_response))

print(batch_response)
