cd /Users/peterdye/ButtBot/butt_detection/models/research
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:/Users/peterdye/ButtBot/butt_detection/models
export PYTHONPATH=$PYTHONPATH:/Users/peterdye/ButtBot/butt_detection/models/reaserch/slim

python object_detection/builders/model_builder_test.py
OR
python object_detection/builders/model_builder_tf2_test.py

# running the training command
cd ssd_mobilenet_v2_320x320_coco17_tpu-8
python ../models/research/object_detection/model_main_tf2.py --model_dir="/Users/peterdye/ButtBot/butt_detection/ssd_mobilenet_v2_320x320_coco17_tpu-8/train" --pipeline_config_path="/Users/peterdye/ButtBot/butt_detection/ssd_mobilenet_v2_320x320_coco17_tpu-8/pipeline.config" --alsologtostderr

# exporting the model / inference graph
cd ssd_mobilenet_v2_320x320_coco17_tpu-8
python ../models/research/object_detection/exporter_main_v2.py \
    --input_type image_tensor \
    --pipeline_config_path ./pipeline.config \
    --trained_checkpoint_dir train \
    --output_directory fine_tuned_model


# ecetesla
To activate buttbot_env:
cd butt_detection
source buttbot_env/bin/activate

To run tensorboard:
ssh -L 16006:127.0.0.1:6006 pjadye@eceubuntu4
activate virtual environment
tensorboard --logdir /path/
on local browser go to 127.0.0.1:16006


# tmux
tmux new -s my_session
ctrl-b, d
tmux ls
tmux attach-session -t my_session
tmux kill-session -t my_session
