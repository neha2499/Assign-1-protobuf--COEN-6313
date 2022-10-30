from flask import Flask, request
from batch_reponse import BatchResponse
import buf_pb2


app = Flask(__name__)


@app.route('/get_batches', methods=['GET'])
def get_batches():
    batch_request = buf_pb2.Request.FromString(request.data)
    batch_response = buf_pb2.Response()
    batch_object = BatchResponse(batch_request.id, batch_request.bench_type, batch_request.metric,
                                 batch_request.batch_unit, batch_request.batch_id, batch_request.batch_size, batch_request.analysis_parameter)
    # result = batch_object.binary_result()
    # print(result)
    result = batch_object.binary_result()
    batch_response.id = result['rfw_id']
    batch_response.last_batch_id = result['last_batch_id']
    batches = result['batches']
    for batch in batches:
        proto_batch = buf_pb2.Batch()
        samples_arr = []
        for i in range(0, len(batch)):
            samples_arr.append(batch[list(batch.keys())[0]])
        proto_batch.samples[:] = samples_arr
        batch_response.batches.append(proto_batch)
        
    batch_response.analysis=result['analysis']
    

    if batch_response is not None and batch_response.last_batch_id is not None:
        searlized_batch_res = batch_response.SerializeToString()
        return searlized_batch_res
    else:
        return "Internal Server Error Occured "


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
