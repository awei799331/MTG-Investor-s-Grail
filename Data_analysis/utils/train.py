import torch
import torch.nn as nn
import torch.optim as optim
import time
import sys
import datetime

######################################################################################
#                         BOILERPLATE CODE, NOT ADAPTED                              #
######################################################################################

def format_time(elapsed):
    # formats time :)
    elapsed_rounded = int(round((elapsed)))
    return str(datetime.timedelta(seconds=elapsed_rounded))

def train(model, dataloader, epochs=1, loss_fn=None, optimizer=None, lr=0.0001, callbacks=[], device=None, callback_args={}):
    # define default loss functions and optimizer
    if loss_fn is None:
        loss_fn = nn.MSELoss() #x is (batch_size, classes), targets are integers that correspond to the index of class (batch_size,)
    if optimizer is None:
        optimizer = optim.Adam(model.parameters(), lr=lr)

    # find device
    if device is None:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model.to(device)

    loss_vals = [] # creating list to store loss values

    callback_outputs = []

    for epoch in range(epochs):
        print("")
        print('======== Epoch {:} / {:} ========'.format(epoch + 1, epochs))
        print('Training...')
        # setting model to training mode
        model.train()
        
        t0 = time.time() # keep track of time taken
        running_loss = 0.0 # keep track of running loss
        
        # training model
        for i, data in enumerate(dataloader):
            inputs, label = data["vec"].to(device), data["price"].to(device)

            optimizer.zero_grad()

            output = model(inputs)

            loss = loss_fn(output, label)
            loss.backward()
            optimizer.step()

            # keeping track of a running loss
            running_loss += loss.item()

            # report progress for each batch
            if not i == 0:
                elapsed = format_time(time.time() - t0)
                
                # Report progress.
                sys.stdout.write("\r" + '  Batch {:>5,}  of  {:>5,}.    Loss: {:.2f}     Elapsed: {:}.'.format(i+1, len(dataloader), loss.item(), elapsed))

        #calculating the average training loss
        avg_train_loss = running_loss / len(dataloader)
        loss_vals.append(avg_train_loss)
        #printing updates
        print("")
        print("  Average training loss: {0:.2f}".format(avg_train_loss))
        print("  Training epoch took: {:}".format(format_time(time.time() - t0)))
    
        callback_args["loss"] = avg_train_loss
        callback_args["epoch"] = epoch + 1
        callback_args["model"] = model
        callback_args["optimizer"] = optimizer
        callback_args["epochs"] = epochs
        callback_args["device"] = device

        callback_returns = []
        for callback in callbacks:
            callback_returns.append(callback(callback_args))
        callback_outputs.append(callback_returns)

    return loss_vals, callback_outputs
