
"""This code was developed as part of article :
"Location games with reputation" by Gaëtan Fournier (Aix-Marseille School of Economics)
and Amaury Francou (École des Mines de Saint-Étienne / Imperial College London).

This program studies the general case with n>=5 players and with cost function
gamma (d) = c * d ^ 2.


Usage:
======
    This code is written in PYTHON

    Usable functions of interest :

    equilibrium_n_players(R,c):  For the given reputation vector R and the strictly
    positive cost function coefficient (c>0), this function verifies if the unique
    equilibrium candidate is an equilibrium.

    probability_Eq_n_players(nb_draws,nb_players,c):   This function estimates the probability
    of existence of an equilibrium by performing several random draws of reputation
    profiles R, and computing the ratio of equilibrium to the number of draws (Eq/nb_draws).

    c_to_probability_n_players(nb_draws,nb_players):  This function plots the ratio obtained
    using probability_Eq_4_players as a function of c in range 0.1 - 10.


"""

__authors__ = ("Gaëtan Fournier", "Amaury Francou")
__contact__ = ("fournier.gtn@gmail.com", "amaury.francou@gmail.com")
__version__ = "1.0.1"
__date__ = "17/06/2022"



import matplotlib.pyplot as plt
import random


##

def delta_distance(c) :

    """Computes the "delta" distance defined in the article.

    As the reputation cost is quadratic, we have delta=1/4c.

    Parameters
    ----------
    c : float
        Cost function coefficient, strictly positive (c>0).

    Returns
    -------
    float
        Computes 1/4c.
    """

    return(1 / (4 * c))

##

def Eq_candidate_n_players(R,c) :

    """This function is specific to n>=5 players game.

    It maps a reputation profile R = [r1,...,rn] to the unique
    equilibrium candidate.

    Parameters
    ----------
    R : list
        Reputation profile vector.

    c : float
        Cost function coefficient, strictly positive (c>0).

    Returns
    -------
    list
        Unique equilibrium candidate.
    """
    nb_players = len(R)

    X=[0 for i in range(nb_players)]  # Initialization of the unique equilibrium candidate.

    delta = delta_distance(c)

    if R[0] + delta < R[1] :
        X[0] = R[0] + delta

    elif R[0] + delta >= R[1] :
        X[0] = R[2] / 3
        X[1] = R[2] / 3

    if R[nb_players - 1] - delta > R[nb_players - 2] :
        X[nb_players - 1] = R[nb_players - 1] - delta

    elif R[nb_players - 1] - delta <= R[nb_players - 2] :
        X[nb_players - 1] = (2 + R[nb_players - 3]) / 3
        X[nb_players - 2] = (2 + R[nb_players - 3]) / 3

    for i in range(1, nb_players - 1) :

        # Only non peripheral players are preset to 0 at this stage.
        if X[i] == 0 :
            X[i] = R[i]

    return(X)

##

def equilibrium_n_players(R,c) :

    """This function is specific to n>=5 players game.

    For the given reputation vector R and the strictly
    positive cost function coefficient (c>0), this function verifies if the unique
    equilibrium candidate is an equilibrium.

    Parameters
    ----------
    R : list
        Reputation profile vector.

    c : float
        Cost function coefficient, strictly positive (c>0).

    Returns
    -------
    string
        Returns the string "Eq" if the candiadte is an equilibrium and "No Eq" otherwise.
    """

    R = sorted(R)
    # We are now considering a sorted reputation profile without loss of generality.

    X = Eq_candidate_n_players(R,c) # The unique equilibrium candidate.

    nb_players = len(X)
    delta = delta_distance(c)

    if X[0] == X[1] :
        if X[0] < R[1]  or  X[0] > R[0] + delta :
            return("No Eq")

    if X[nb_players - 2] == X[nb_players - 1] :
        if X[nb_players - 1] < R[nb_players - 1] - delta  or  R[nb_players - 2] < X[nb_players - 1] :
            return("No Eq")

    # Deviations of Player 1 if alone on his position.
    if X[0] != X[1] :
        payoff = ((X[0] + X[1]) / 2) - (c * ((X[0] - R[0])**2))

        # Deviation to the right of Player n
        if (1 - X[nb_players - 1]) - (c * ((X[nb_players - 1] - R[0])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between two players to his right
        for j in range(1,nb_players - 1) :
            if X[j] == X[j + 1] :
                continue

            if ((X[j + 1] - X[j]) / 2) - (c * ((X[j] - R[0])**2)) > payoff :
                return("No Eq")

    # Deviations of Player 1 and Player 2 if paired
    elif X[0] == X[1] :

        # Deviations of Player 1 if paired with Player 2
        payoff = ((X[0] + X[2]) / 4) - (c * ((X[0] - R[0])**2))

        # Deviation to the right of Player n
        if (1 - X[nb_players - 1]) - (c * ((X[nb_players - 1] - R[0])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between two players to his right
        for j in range(2,nb_players - 1) :
            if X[j] == X[j + 1] :
                continue

            if ((X[j + 1] - X[j]) / 2) - (c * ((X[j] - R[0])**2)) > payoff :
                return("No Eq")

        # Deviations of Player 2 if paired with Player 1
        payoff = ((X[0] + X[2]) / 4) - (c * ((X[0] - R[1])**2))

        # Deviation to the right of Player n
        if (1 - X[nb_players - 1]) - (c * ((X[nb_players - 1] - R[1])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between two players to his right
        for j in range(2,nb_players - 1) :
            if X[j] == X[j + 1] :
                continue

            if ((X[j + 1] - X[j]) / 2) - (c * ((X[j] - R[1])**2)) > payoff :
                return("No Eq")

    # Deviations of Player n if alone on his position.
    if X[nb_players - 1] != X[nb_players - 2] :
        payoff = (1 - ((X[nb_players - 1] + X[nb_players - 2]) / 2)) - (c * ((X[nb_players - 1] - R[nb_players - 1])**2))

        # Deviation to the left of Player 1
        if X[0] - (c * ((X[0] - R[nb_players - 1])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between two players to his left
        for j in range(1,nb_players - 1) :
            if X[j] == X[j - 1] :
                continue

            if ((X[j] - X[j - 1]) / 2) - (c * ((X[j] - R[nb_players - 1])**2)) > payoff :
                return("No Eq")

    # Deviations of Player n and Player n-1 if paired
    elif X[nb_players - 1] == X[nb_players - 2] :

        # Deviations of Player n if paired with Player n-1
        payoff = (0.5 - ((X[nb_players - 1] + X[nb_players - 3]) / 4)) - (c * ((X[nb_players - 1] - R[nb_players - 1])**2))

        # Deviation to the left of Player 1
        if X[0] - (c * ((X[0] - R[nb_players - 1])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between two players to his left
        for j in range(1,nb_players - 2) :

            if X[j] == X[j - 1] :
                continue

            if ((X[j] - X[j - 1]) / 2) - (c * ((X[j] - R[nb_players - 1])**2)) > payoff :
                return("No Eq")

        # Deviations of Player n-1 if paired with Player n
        payoff = (0.5 - ((X[nb_players - 1] + X[nb_players - 3]) / 4)) - (c * ((X[nb_players - 1] - R[nb_players - 2])**2))

        # Deviation to the left of Player 1
        if X[0] - (c * ((X[0] - R[nb_players - 2])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between two players to his left
        for j in range(1,nb_players - 2) :

            if X[j] == X[j - 1] :
                continue

            if ((X[j] - X[j - 1]) / 2) - (c * ((X[j] - R[nb_players - 2])**2)) > payoff :
                return("No Eq")

    # Deviations of Player p with  1 < p < n, if not paired.
    for p in range(1,nb_players - 1) :

        if X[p - 1] == X[p]  or  X[p] == X[p + 1] :
            continue
            # Considering not paired players


        payoff = ((X[p + 1] - X[p - 1]) / 2)
        # Deviation to the left of Player 1

        if X[0] - (c * ((X[0] - R[p])**2)) > payoff :
            return("No Eq")

        # Deviation to the right of Player n
        if (1 - X[nb_players - 1]) - (c * ((X[nb_players - 1] - R[p])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between two players to his left
        for j in range(1,p) :
            if X[j] == X[j - 1] :
                continue

            if ((X[j] - X[j - 1]) / 2) - (c * ((X[j] - R[p])**2)) > payoff :
                return("No Eq")

         # Deviations in the interval in between two players to his right
        for j in range(p + 1,nb_players - 1) :
            if X[j] == X[j + 1] :
                continue

            if ((X[j + 1] - X[j]) / 2) - (c * ((X[j] - R[p])**2)) > payoff :
                return("No Eq")

    return("Eq")

##

def probability_Eq_n_players(nb_draws,nb_players,c) :

    """This function is specific to n>=5 players game.

    This function estimates the probability
    of existence of an equilibrium by performing several random draws of reputation
    profiles R, and computing the ratio of equilibrium to the number of draws (Eq/nb_draws).

    Parameters
    ----------
    nb_draws : int
        Number of draws requested.

    nb_players : int
        Number of players requested >=5.

    c : float
        Cost function coefficient, strictly positive (c>0).

    Returns
    -------
    float
        Returns the ratio of equilibrium to the number of draws (Eq/nb_draws).
    """

    Eq = 0 # Counts the number of Nash equilibrium

    for i in range(nb_draws) :

        R=[random.random() for p in range(nb_players)]
        # Draw a reputation profile, i.e. a list of nb_players real numbers between 0 and 1.

        if equilibrium_n_players(R,c) == "Eq" :
            Eq += 1

    return(Eq / nb_draws)

##

def c_to_probability_n_players(nb_draws,nb_players) :

    """This function is specific to n>=5 players game.

    This function plots the ratio obtained
    using probability_Eq_4_players as a function of c in range 0.1 - 10.

    Parameters
    ----------
    nb_draws : int
        Number of draws requested.

    nb_players : int
        Number of players requested >=5.


    Returns
    -------
    None
        Plots the ratio of equilibrium to the number of draws (Eq/nb_draws) as
    a function of c.
    """


    c_set = [] # Set of different c coefficients to be the X axis.
    Eq_set = [] # Set of Eq/nb_draws ratio to be the Y axis.


    for j in range(5) :
    # Thinner plotting around the five first integers
        for i in range(10) :
            if j + (i / 10) == 0 :
                continue
                # The cost function is definded for c>0.

            c_set += [j + (i / 10)]
            Eq_set += [probability_Eq_n_players(nb_draws,nb_players,j + (i / 10))]


    # The reader may change these plotting parameters.
    for j in range(5,15) :
        c_set += [j]
        Eq_set += [probability_Eq_n_players(nb_draws,nb_players,j)]


    plt.scatter(c_set,Eq_set)
    plt.xlabel('c')
    plt.ylabel('Probability of equilibrium')
    plt.show()
