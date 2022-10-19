import numpy as np
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt # for part 3

def rng(len): # Random number generator
    rng = np.random.default_rng()
    rints = rng.integers(low=0, high=len)
    return(rints)


def k_means(data, num_of_k, kavg = []): # k_means function

    # --- Initializing Variables --- #
    num_k = num_of_k - 1
    num = []
    while num_k != -1:
        num.append(num_k)
        num_k -= 1
    num.reverse() # Should be an array from 0 -> num of k - 1
    num_k = num_of_k - 1
    k = kavg
    distance = [] # Num_of_k arrays that are each arrays holding distance between respective k and each data point
    assign_k = [] # Assign each data point to a k by comparing distance
    avgk = [] # Array of sums of all vectors related to respective centroid
    how_many_k = [] # Number of datapoints per k
    new_avg_k = [] # Final average of all centroids (new coordinate for successive runs)

    # Check if k array is empty (necessary for running function multiple times in a row)
    if not k:
        for n in range(num_of_k): # Creating matrix of k's that use random datapoints if no existing k is found
            a = rng(len(data))
            k.append(data[a])

    # For loop that calculates and appends distances from each datapoint to each k
    for n in range(num_of_k):
        temp = []
        for m in range(len(data)):
            a = []
            for i in range(len(data[0])):
                b = k[n][i] - data[m][i] # Difference between k_n and data pointwait

                a.append(b*b) # Add square of difference to a
            temp.append(np.sqrt(sum(a))) #  Append 2-norm to temp array (distance between k and datapoint)
        distance.append(temp)

    # Assigning Datapoints to a Centroid
    for n in range(len(distance[0])): # Make temp array to compare all num in same dimension
        temp_array = []
        for i in range(len(distance)):
            temp_array.append(distance[i][n]) # Find min of temp array
        a = np.amin(temp_array)  # Set min to variable
        index_temp = []
        for i in range(len(temp_array)): # Check temp array for min variable to find the index (which corresponds to the centroid)
            if a == temp_array[i]:
                index_temp.append(i)
        if len(index_temp) > 1: # Checks for multiple min values
            assign_k.append(index_temp[rng(len(index_temp))]) # Randomly assigns the repeating min value to a random index
        else:
            assign_k.append(index_temp[0])

    # Summing correlated datapoints from each respective centroid
    for i in range(num_of_k):
        temp = [0]*len(data[0]) # Temporary zero vector
        count = 0 # Count how many datapoints belong to each centroid
        for n in range(len(assign_k)):
            if assign_k[n] == num[i]: # If belongs to that centroid, then add the datapoint values at index to centroid (temp array)
                count += 1
                temp = np.add(temp, data[n])
        avgk.append(temp)
        how_many_k.append(count)

    # Average value calculation
    for i in range(len(avgk)): # Divides by number of terms to get avg for each dimension
        if how_many_k[i] != 0:
            mean_k = np.divide(avgk[i], how_many_k[i])
            new_avg_k.append(mean_k)
        else:
            continue

    # Recursion so function runs until centroids have all been found
    if np.array_equal(new_avg_k, kavg) == True:
        return(assign_k, new_avg_k)
    else:
        return(k_means(data, num_of_k, new_avg_k))



if __name__ == "__main__":

    # --- Initializing --- #
    x_axis = [] # For graphs later
    y_axis = [] # Final answer
    index = []
    centroid_pos = []

    # Question 1
    # data = load_breast_cancer()
    # print(k_means(data.data, 7))

    # Question 2 & 3
    for i in range(2, 8):
        x_axis.append(i)
        index, centroid_pos = k_means(data.data, i, []) # Q1.2
        arr = [] # Array of distance calculations, to be summed later
        for n in range(i): # for each centroid i = 2-7
            temp = 0
            for m in range(len(index)): # Scan through the index array to check index num (which centroid) m = 1-569
                if n == index[m]:# If belongs to centroid i
                    for z in range(len(data.data[0])): # For each dimension
                        temp += np.square(data.data[m][z] - centroid_pos[n][z]) # square the difference between each datapoint and centroid
                    arr.append(temp)
        a = np.sum(arr)
        a = a / len(data.data)
        y_axis.append(a)

    # Graphing
    plt.plot(x_axis,y_axis,"o")
    plt.title("Distortion vs. Number of Centroids")
    plt.xlabel("Number of Centroids (k)")
    plt.ylabel("Distortions")
    plt.show()



