import torch
import gc

print(torch.cuda.is_available()) 
print(torch.cuda.get_device_name(0)) 

# Python のガベージコレクタで不要なオブジェクトを回収
gc.collect()

# PyTorch に GPU キャッシュを明示的に解放させる
torch.cuda.empty_cache()
torch.cuda.ipc_collect()
