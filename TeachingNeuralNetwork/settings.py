epochs = 100
batch = 64
monitor='val_accuracy'
mode='max'
test_size = 0.2
optimizer='adam'
loss='binary_crossentropy' #'huber'