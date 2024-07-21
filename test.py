
from onnx2torch import convert
import onnx
# Path to ONNX model
onnx_model_path = "weights.onnx" # this is for a test model that i tried to rip from roboflowuniverse
onnx_model = onnx.load(onnx_model_path)
torch_model_2 = convert(onnx_model)