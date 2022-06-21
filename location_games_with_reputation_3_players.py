
"""This code was developed as part of article :
"Location games with reputation" by Gaëtan Fournier (Aix-Marseille School of Economics)
and Amaury Francou (École des Mines de Saint-Étienne / Imperial College London).

This program studies the case of three players (n=3) with the cost function
gamma (d) = c * d ^ 2.

Usage:
======
    This code is written in PYTHON

    Usable functions of interest :

    equilibrium_3_players(R,c):  For the given reputation vector R and the strictly
    positive cost function coefficient (c>0), this function verifies if the unique
    equilibrium candidate is an equilibrium.

    probability_Eq_3_players(nb_draws,c):   This function estimates the probability
    of existence of an equilibrium by performing several random draws of reputation
    profiles R, and computing the ratio of equilibrium to the number of draws (Eq/nb_draws).

    c_to_probability_3_players(nb_draws):  This function plots the ratio obtained
    using probability_Eq_3_players as a function of c in range 0.1 - 10.

    Eq_plot_3_players(nb_draws,c,r_set) : This function performs several
    random draws of (ri,rj) and plots the couples for which the game with
    reputation vector R = [r_set, ri, rj] admits an equilibrium.

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

def Eq_candidate_3_players(R,c) :

    """This function is specific to n=3 players game.

    It maps a reputation profile R = [r1,r2,r3] to the unique
    equilibrium candidate if any. The function returns "No Eq" otherwise.

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

    or string
        If there are no equilibrium returns "No Eq".
    """

    X=[0,0,0]  # Initialization of the unique equilibrium candidate.
    delta = delta_distance(c)


    if R[0] + delta < R[1] and R[2] - delta > R[1] :
        X[0] = R[0] + delta
        X[1] = R[1]
        X[2] = R[2] - delta

    elif R[0] + delta >= R[1] and R[2] - delta > R[1] :
        X[0] = (R[2] - delta) / 3
        X[1] = (R[2] - delta) / 3
        X[2] = R[2] - delta

    elif R[2] - delta <= R[1] and R[0] + delta < R[1] :
        X[0] = R[0] + delta
        X[1] = (R[0] + delta +2) / 3
        X[2] = (R[0] + delta + 2) / 3

    else :
        return("No Eq")

    return(X)



##

def equilibrium_3_players(R,c) :

    """This function is specific to n=3 players game.

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


    R=sorted(R)
    # We are now considering a sorted reputation profile without loss of generality.

    X =  Eq_candidate_3_players(R,c)

    if X == "No Eq" :
        return("No Eq")

    delta = delta_distance(c)


    if X[0] == X[1] :
        if X[0] < R[1]  or  X[0] > R[0] + delta :
            return("No Eq")


    if X[1] == X[2] :
        if X[2] < R[2] - delta  or  R[1] < X[2] :
            return("No Eq")


    # Deviations of Player 1 if alone on his position.
    if X[0] != X[1] :
        payoff = ((X[0] + X[1]) / 2) - (c * ((X[0] - R[0])**2))

        # Deviation to the right of Player 3
        if (1 - X[2]) - (c * ((X[2] - R[0])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between Player 2 and Player 3
        if X[1] != X[2] and ((X[2] - X[1]) / 2) - (c * ((X[1] - R[0])**2)) > payoff :
            return("No Eq")


    # Deviations of Player 1 and Player 2 if paired
    elif X[0] == X[1] :

        # Deviations of Player 1 if paired with Player 2
        payoff = ((X[0] + X[2]) / 4) - (c * ((X[0] - R[0])**2))

        # Deviation to the right of Player 3
        if (1 - X[2]) - (c * ((X[2] - R[0])**2)) > payoff :
            return("No Eq")

        # Deviations of Player 2 if paired with Player 1
        payoff = ((X[0] + X[2]) / 4) - (c * ((X[0] - R[1])**2))

        # Deviation to the right of Player 3
        if (1 - X[2]) - (c * ((X[2] - R[1])**2)) > payoff :
            return("No Eq")

    # Deviations of Player 3 if alone on his position.
    if X[2] != X[1] :

        payoff = (1 - ((X[2] + X[1]) / 2)) - (c * ((X[2] - R[2])**2))
        # Deviation to the left of Player 1

        if X[0] - (c * ((X[0] - R[2])**2)) > payoff :
            return("No Eq")

        # Deviations in the interval in between Player 1 and Player 2
        if X[1] != X[0] and ((X[1] - X[0]) / 2) - (c * ((X[1] - R[2])**2)) > payoff :
            return("No Eq")

    # Deviations of Player 3 and Player 2 if paired

    elif X[2] == X[1] :
        # Deviations of Player 3 if paired with Player 2

        payoff = (0.5 - ((X[2] + X[0]) / 4)) - (c * ((X[2] - R[2])**2))
        # Deviation to the left of Player 1

        if X[0] - (c * ((X[0] - R[2])**2)) > payoff :
            return("No Eq")

        # Deviations of Player 2 if paired with Player 3
        payoff = (0.5 - ((X[2] + X[0]) / 4)) - (c * ((X[2] - R[1])**2))

        # Deviation to the left of Player 1
        if X[0] - (c * ((X[0] - R[1])**2)) > payoff :
            return("No Eq")


    # Deviations of Player 2, if not paired.

    if X[0] != X[1]  and  X[1] != X[2] :
    # Considering not paired players

        payoff = ((X[2] - X[0]) / 2)
        # Deviation to the left of Player 1

        if X[0] - (c * ((X[0] - R[1])**2)) > payoff :
            return("No Eq")

        # Deviation to the right of Player 3
        if (1 - X[2]) - (c * ((X[2] - R[1])**2)) > payoff :
            return("No Eq")

    return("Eq")




##

def probability_Eq_3_players(nb_draws,c) :

    """This function is specific to n=3 players game.

    This function estimates the probability
    of existence of an equilibrium by performing several random draws of reputation
    profiles R, and computing the ratio of equilibrium to the number of draws (Eq/nb_draws).

    Parameters
    ----------
    nb_draws : int
        Number of draws requested.

    c : float
        Cost function coefficient, strictly positive (c>0).

    Returns
    -------
    float
        Returns the ratio of equilibrium to the number of draws (Eq/nb_draws).
    """

    Eq = 0 # Counts the number of equilibrium

    for i in range(nb_draws) :

        R=[random.random() for p in range(3)]
        # Draw a reputation profile, i.e. a list of 3 real numbers between 0 and 1.

        if equilibrium_3_players(R,c) == "Eq" :
            Eq += 1

    return(Eq / nb_draws)



##

def c_to_probability_3_players(nb_draws) :

    """This function is specific to n=3 players games.

    This function plots the ratio obtained
    using equilibrium_3_players as a function of c in range 0.1 - 10.

    Parameters
    ----------
    nb_draws : int
        Number of draws requested.

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
            Eq_set += [probability_Eq_3_players(nb_draws,j + (i / 10))]

    # The reader may change these plotting parameters.
    for j in range(5,11) :
        c_set += [j]
        Eq_set += [probability_Eq_3_players(nb_draws,j)]


    plt.scatter(c_set,Eq_set)
    plt.xlabel('c')
    plt.ylabel('Probability of equilibrium')
    plt.show()



##

def Eq_plot_3_players(nb_draws,c,r_set) :

    """This function is specific to n=3 players game.

    This function performs several
    random draws of (ri,rj) and plots the couples for which the game with
    reputation vector R = [r_set, ri, rj] admits an equilibrium.

    Parameters
    ----------
    nb_draws : int
        Number of draws requested.

    c : float
        Cost function coefficient, strictly positive (c>0).

    r_set : float
        Requested set reputation, real number between 0 and 1.

    Returns
    -------
    None
        Plots the (ri, rj) couples for which the sorted reputation vector
    R = [r_set, ri, rj] admits an equilibrium.
    """


    Ri = [] # Set of different ri reputations to be the X axis.
    Rj = [] # Set of different rj reputations to be the Y axis.

    stock_1 = 0 # Storage variable
    stock_2 = 0

    for i in range(nb_draws) :

        R = [random.uniform(0, 1) ,random.uniform(0, 1),r_set]
        # Two real numbers between 0 and 1 are drawn and stacked with
        # the preset reputation.

        stock_1 = R[0]
        stock_2 = R[1]

        # As the R vector will be sorted it is necessary to store the drawn reputations.
        if equilibrium_3_players(R,c) == "Eq" :
            Ri += [stock_1]
            Rj += [stock_2]



    # The variable s allows the user to adjust the size of the points on the figure.
    plt.scatter(Ri,Rj,s=1)
    plt.xlabel('ri')
    plt.ylabel('rj')
    plt.show()
