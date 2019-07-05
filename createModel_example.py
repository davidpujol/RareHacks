import pandas as pd
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from keras import backend as K
from random import shuffle


#DATA TREATMENT

#we read the csv file. The first bit is the label and the rest are the pixels (for each image)
allImages = pd.read_csv('/Users/david/Documents/ImageRecognition/Handwritting/A_Z Handwritten Data.csv').values


#SHUFFLE THE INITIAL SET
shuffle(allImages)


#reshape them into a 4D matrix (pass from (372450,785) to (372450,1,28,28) (4D because of the convolution2D Layer)
X = allImages[:,1:].reshape(allImages.shape[0],1,28,28).astype('float32')
X = X / 255 #range of 0-1

Y = allImages[:,0]

#we cannot pass an N size vector but an NxM matrix (N is num of training examples and M is the number of categories)
Y = to_categorical(Y)	


#EXTRACT TRAINING AND VALIDATION SET
elements_train = int(allImages.shape[0] * 0.8)
X_train = X[0:elements_train,:,:,:]
Y_train = Y[0:elements_train,:]

X_test = X[elements_train+1:,:,:,:]
Y_test = Y[elements_train+1:,:]


#MODEL

#Let's build our neural network (every line is a layer)
model = Sequential()
K.set_image_dim_ordering('th')
model.add(Convolution2D(30, 5, 5, border_mode= 'valid' , input_shape=(1,28, 28),activation= 'relu' ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(15, 3, 3, activation= 'relu' ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(128, activation= 'relu' ))
model.add(Dense(50, activation= 'relu' ))
model.add(Dense(26, activation= 'softmax' ))	#output layer
 

# Compile model (used to keep changing the weight of our neural network for every pass to keep reducing the loss, normaly using gradient descent or some other optimization)
model.compile(loss= 'categorical_crossentropy' , optimizer= 'adam' , metrics=[ 'accuracy' ])


#TRAINING

#Let's fit the data to our model
model.fit(X_train, Y_train,validation_data=(X_test,Y_test), epochs=5, batch_size=160)	#we use automatic data split for validation

#SAVE THE MODEL
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

