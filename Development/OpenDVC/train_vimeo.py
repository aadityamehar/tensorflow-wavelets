import OpenDVC
import numpy as np
import load
import tensorflow as tf
import matplotlib.pyplot as plt

tf.executing_eagerly()

batch_size = 1
EPOCHS = 20
Height = 240
Width = 240
Channel = 3
lr_init = 1e-4
samples = 200
I_QP=27

model = OpenDVC.OpenDVC(width=Width, height=Height, batch_size=batch_size, num_filters=128)
# model.summary()
model.compile()
print("* [Model compiled]...")
args = OpenDVC.Arguments()

# folder = np.load("/mnt/WindowsDev/Developer/tensorflow-wavelets/folder_cloud.npy")
# data = load.load_data_vimeo90k(samples, batch_size, Height, Width, Channel, folder, I_QP)
data = load.load_data_vimeo90k("/mnt/WindowsDev/Developer/tensorflow-wavelets/folder_cloud.npy",
                                samples, Height, Width, Channel, I_QP)

dataset = tf.data.Dataset.from_tensor_slices(data)

# model.load_weights(args.model_checkpoints)

print("Going to fit")
model.fit(
        dataset,
        epochs=EPOCHS, 
        verbose=1, 
        callbacks=
            [
            OpenDVC.MemoryCallback(),
            tf.keras.callbacks.ModelCheckpoint(filepath=args.model_checkpoints, save_weights_only=True, save_freq='epoch', monitor='train_loss_MV', mode='max', save_best_only=True), 
            tf.keras.callbacks.TerminateOnNaN(),
            tf.keras.callbacks.TensorBoard(log_dir=args.backup_restore, histogram_freq=0, update_freq="epoch"),
            tf.keras.callbacks.experimental.BackupAndRestore(args.backup_restore),
            ],

        )  

print("Done Training ...")
tf.saved_model.save(model, args.model_save)
print("saved", args.model_save)