import tensorflow as tf

output_saved_model_dir = './tensorrt_model'

# Option 1
params = tf.experimental.tensorrt.ConversionParams(
    precision_mode='FP16')
converter = tf.experimental.tensorrt.Converter(
    input_saved_model_dir="my_dir", conversion_params=params)
converter.convert()
converter.save(output_saved_model_dir)


# Option 2
# params = tf.experimental.tensorrt.ConversionParams(
#     precision_mode='FP16',
#     # Set this to a large enough number so it can cache all the engines.
#     maximum_cached_engines=16)
# converter = tf.experimental.tensorrt.Converter(
#     input_saved_model_dir="my_dir", conversion_params=params)
# converter.convert()
#
# # Define a generator function that yields input data, and use it to execute
# # the graph to build TRT engines.
# # With TensorRT 5.1, different engines will be built (and saved later) for
# # different input shapes to the TRTEngineOp.
# # def my_input_fn():
# #     for _ in range(num_runs):
# #         inp1, inp2 = ...
# #         yield inp1, inp2
#
# converter.build(input_fn=my_input_fn)  # Generate corresponding TRT engines
# converter.save(output_saved_model_dir)  # Generated engines will be saved.
