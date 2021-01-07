from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf


def load_graph(model_file_):
    graph_ = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file_, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph_.as_default():
        tf.import_graph_def(graph_def)

    return graph_


def read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255):
    file_reader = tf.read_file(file_name, "file_reader")
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels=3, name='png_reader')
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name='gif_reader'))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels=3, name='jpeg_reader')
    dims_expander = tf.expand_dims(tf.cast(image_reader, tf.float32), 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    return tf.Session().run(tf.divide(tf.subtract(resized, [input_mean]), [input_std]))


def get_NN(file, param):
    file_name = f"media/{file}"

    graph = load_graph(f"neuronetwork/{param}.pb")
    t = read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255)

    input_operation = graph.get_operation_by_name("import/Mul")
    output_operation = graph.get_operation_by_name("import/final_result")

    with tf.Session(graph=graph) as sess:
        results = np.squeeze(sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t}))

    data = {}
    full = 0
    for i, result in enumerate(results):
        if param == "age":
            data[f"{i * 10}-{i * 10 + 10}"] = float(result)
            full += float(result) * float(i * 10)
        elif param == "gender":
            data[f"{i}"] = float(result)
        full += float(result) * float(i)
    data[param] = full
    return data


if __name__ == "__main__":
    get_NN("image.png", "age")
