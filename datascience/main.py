from pandas import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline is a Jupyter magic command and not valid in scripts
plt.ion()  # Enables interactive mode for matplotlib

def main():
    data_filename = "advertising.csv"
    df = pd.read_csv(data_filename)

    # Display full data set
    print("Full DataFrame:")
    print(df)

    # Get a quick look of the data
    print("\nDataFrame info:")
    print(df.info())

    # Create a new dataframe with only the first 7 rows
    df_subset = df.iloc[:7]
    print("\nSubset of DataFrame:")
    print(df_subset)

    # Use a scatter plot for plotting a graph of TV vs Sales
    plt.scatter(df['TV'], df['Sales'])
    plt.title("TV vs Sales")
    plt.xlabel("TV")
    plt.ylabel("Sales")
    plt.show()



    # Display the shape of the DataFrame
    print("\nDataFrame shape:")
    print(df.shape)

    # Get a quick look of the data
    # read from console so application doesn't end
    read = input("Press Enter to continue...")


if __name__ == "__main__":
    main()
