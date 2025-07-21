import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split


def main():
    filename = 'Advertising.csv'
    df_adv = pd.read_csv(filename)

    df_adv.head()
    df_adv.info()
    input("Press Enter to continue...")




if __name__ == "__main__":
    main()