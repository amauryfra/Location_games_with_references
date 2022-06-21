
"""This code was developed as part of article :
"Location games with reputation" by Gaëtan Fournier (Aix-Marseille School of Economics)
and Amaury Francou (École des Mines de Saint-Étienne / Imperial College London).

This program studies the case of two players (n=2) with the cost function
gamma (d) = c * d ^ 2.


Usage:
======
    This code is written in PYTHON

    Usable functions of interest :

    equilibrium_2_players(R,c):  For the given reputation vector R and the strictly
    positive cost function coefficient (c>0), this function verifies if the unique
    equilibrium candidate is an equilibrium.

    probability_Eq_2_players(nb_draws,c):   This function estimates the probability
    of existence of an equilibrium by performing several random draws of reputation
    profiles R, and computing the ratio of equilibrium to the number of draws (Eq/nb_draws).

    c_to_probability_2_players(nb_draws):  This function plots the ratio obtained
    using probability_Eq_2_players as a function of c in range 0.1 - 10.

    Eq_plot_2_players(nb_draws,c) : This function performs several
    random draws of (r1,r2) and plots the couples for which there exists
    an equilibrium.

    equilibrium_2_players_asym(R,c1,c2):  For the given reputation vector R and the
    strictly positive cost function coefficients (c1>0 and c2>0) - that are here
    specific to each players - this function verifies if the unique
    equilibrium candidate is an equilibrium.

    Eq_plot_2_players_asym(nb_draws,c1,c2) : This function performs several
    random draws of (r1,r2) and plots the couples for which there exists
    a equilibrium, assuming two separate cost function coefficients (c1 and c2)
    specific to each player.


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

def equilibrium_2_players(R,c) :

    """This function is specific to n=2 players game.

    It checks wether the unique equilibrium candidate is an equilibrium.

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

    delta = delta_distance(c)

    X = [0,0] # Initialization of the unique equilibrium candiadte.


    if R[1] - R[0] < 2 * delta :

        if R[1] - delta < (1 / 2) and (1 / 2) < R[0] + delta :
            return("Eq")
        else :
            return("No Eq")


    else :

        X[0] = R[0] + delta
        X[1] = R[1] - delta

        if 1 - X[1] - c * (X[1]-R[0])**2 < ((X[0] + X[1]) / 2) \
        - c * (X[0] - R[0])**2 and X[0] - c * (X[0] - R[1])**2 < 1 \
        - ((X[0] + X[1]) / 2) - c * (X[1]-R[1])**2 :
            return("Eq")

        else :
            return("No Eq")




##

def probability_Eq_2_players(nb_draws,c) :

    """This function is specific to n=2 players game.

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

        R=[random.random() for p in range(2)]
        # Draw a reputation profile, i.e. a list of 2 real numbers between 0 and 1.

        if equilibrium_2_players(R,c) == "Eq" :
            Eq += 1

    return(Eq / nb_draws)


##

def c_to_probability_2_players(nb_draws) :

    """This function is specific to n=2 players game.

    This function plots the ratio obtained
    using probability_Eq_2_players as a function of c in range 0.1 - 10.

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
            Eq_set += [probability_Eq_2_players(nb_draws,j + (i / 10))]


    # The reader may change these plotting parameters.
    for j in range(5,11) :

        c_set += [j]
        Eq_set += [probability_Eq_2_players(nb_draws,j)]


    plt.scatter(c_set,Eq_set)
    plt.xlabel('c')
    plt.ylabel('Probability of equilibrium')
    plt.show()



##

def Eq_plot_2_players(nb_draws,c) :

    """This function is specific to n=2 players game.

    This function performs several random draws of (r1,r2) and
    plots the couples for which there exists an equilibrium.


    Parameters
    ----------
    nb_draws : int
        Number of draws requested.

    c : float
        Cost function coefficient, strictly positive (c>0).


    Returns
    -------
    None
        Plots the (r1, r2) couples for which there exists an equilibrium.
    """

    R1 = [] # Set of different r1 reputations to be the X axis.
    R2 = [] # Set of different r2 reputations to be the Y axis.

    for i in range(nb_draws) :

        R = [random.uniform(0, 1) ,random.uniform(0, 1)]
        # Two real numbers between 0 and 1 are drawn.

        if equilibrium_2_players(R,c) == "Eq" :
            R1 += [R[0]]
            R2 += [R[1]]


    # The variable s allows the user to adjust the size of the points on the figure.
    plt.scatter(R1,R2,s=1)
    plt.xlabel('r1')
    plt.ylabel('r2')
    plt.show()


##


def equilibrium_2_players_asym(R,c1,c2) :

    """This function is specific to n=2 players game.

    For the given reputation vector R and the
    strictly positive cost function coefficients (c1>0 and c2>0) - that are here
    specific to each players - this function verifies if the unique
    equilibrium candidate is an equilibrium.

    Parameters
    ----------
    R : list
        Reputation profile vector.

    c1 : float
        Cost function coefficient specific to Player 1, strictly positive (c1>0).

    c2 : float
        Cost function coefficient specific to Player 2, strictly positive (c2>0).

    Returns
    -------
    string
        Returns the string "Eq" if the candiadte is an equilibrium and "No Eq" otherwise.
    """

    R = sorted(R)
    # We are now considering a sorted reputation profile without loss of generality.

    delta1 = delta_distance(c1)
    delta2 = delta_distance(c2)

    X = [0,0] # Initialization of the equilibrium candidate.


    if R[1] - R[0] < delta1 + delta2 :

        if R[1] - delta2 < (1 / 2) and (1 / 2) < R[0] + delta1 :
            return("Eq")

        else :
            return("No Eq")


    else :

        X[0] = R[0] + delta1
        X[1] = R[1] - delta2

        if 1 - X[1] - c1 * (X[1]-R[0])**2 < ((X[0] + X[1]) / 2) \
        - c1 * (X[0] - R[0])**2 and X[0] - c2 * (X[0] - R[1])**2 < 1 \
        - ((X[0] + X[1]) / 2) - c2 * (X[1]-R[1])**2 :
            return("Eq")

        else :
            return("No Eq")


##

def Eq_plot_2_players_asym(nb_draws,c1,c2) :

    """This function is specific to n=2 players game.

    This function performs several
    random draws of (r1,r2) and plots the couples for which there exists
    a equilibrium, assuming two separate cost function coefficients (c1 and c2)
    specific to each player.


    Parameters
    ----------
    nb_draws : int
        Number of draws requested.

    c1 : float
        Cost function coefficient specific to Player 1, strictly positive (c1>0).

    c2 : float
        Cost function coefficient specific to Player 2, strictly positive (c2>0).


    Returns
    -------
    None
        Plots the (r1, r2) couples for which there exists an equilibrium.
    """

    R1 = [] # Set of different r1 reputations to be the X axis.
    R2 = [] # Set of different r2 reputations to be the Y axis.

    for i in range(nb_draws) :

        R = [random.uniform(0, 1) ,random.uniform(0, 1)]
        # Two real numbers between 0 and 1 are drawn.

        if equilibrium_2_players_asym(R,c1,c2) == "Eq" :
            R1 += [R[0]]
            R2 += [R[1]]


    # The variable s allows the user to adjust the size of the points on the figure.
    plt.scatter(R1,R2,s=1)
    plt.xlabel('r1')
    plt.ylabel('r2')
    plt.show()
