import torch
import torch.nn as nn
import time
import copy

######################################################################################
#                         BOILERPLATE CODE, NOT ADAPTED                              #
######################################################################################

def saving_checkpoints_callback(path2chckpt, freq):

    def save(kwargs):
        optimizer = kwargs["optimizer"]
        model = kwargs["model"]
        epoch = kwargs["epoch"]
        epochs = kwargs["epochs"]
        loss = kwargs["loss"]
        if ((epoch - 1) % freq == 0 or epoch == epochs) and ((epoch != 1) or (freq == 1)):
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
                }, "{}/{}epoch_{}loss.pt".format(path2chckpt, epoch, loss))
        
    return save

def store_best_run(path2chckpt):

    def save_best(kwargs):
        model = kwargs["model"]
        epoch = kwargs["epoch"]
        epochs = kwargs["epochs"]
        loss = kwargs["loss"]

        try:
            kwargs["best_loss"]
        except:
            kwargs["best_loss"] = float("inf")

        if loss > kwargs["best_loss"]:
            print("best model so far")
            print(kwargs["best_loss"])
            kwargs["best_loss"] = loss
            kwargs["best_model"] = copy.deepcopy(model)

        if epoch == epochs:
            torch.save({
                'model_state_dict': kwargs["best_model"].state_dict(),
                'loss': kwargs["best_loss"],
                }, "{}/BEST{}acc.pt".format(path2chckpt, kwargs["best_loss"]))
        
    return save_best