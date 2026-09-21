Ce que nous avons appris 

Dans le cadre de ce laboratoire, nous avons appris comment implémenter plusieurs algorithmes de recherche différents comme la recherche en profondeur, en largeur et à approfondissement itératif. De cette façon, il a été possible de pouvoir visualiser ce que représente vraiment la complexité de résolution (autant spatiale que temporelle). En effet, même si notre solution finale résolvait les puzzles dans des délais acceptables, cela n’était pas le cas de notre première version qui continuait pour une longue période. Ensuite, il a également été possible de voir comment traduire un problème réel en une solution par graphe. De plus, nous avons pu apprendre que certains problèmes tels que l'exercice 3 n'avaient pas de solution et donc il était nécessaire d'ajouter un garde-fou afin que l'algorithme ne s'effectue pas à l'infini. 

Comparaison des algorithmes de recherche 

Le tableau ci-dessous représente les performances moyennes des trois algorithmes sur les 4 puzzles (excepté le troisième car le problème est insolvable) et leurs 10 itérations. 


Algorithme : Largeur 

Temps moyen (s) : 4,17 

Nombre d’état exploré moyen : 85720 

Taille de la file frontière moyenne : 9676 


Algorithme : Profondeur 

Temps moyen (s) : 2,74 

Nombre d’état exploré moyen : 64291 

Taille de la file frontière moyenne : 42993 


Algorithme : Approfondissement itératif (10 de profondeur) 

Temps moyen (s) : 0,021 

Nombre d’état exploré moyen : 2239 

Taille de la file frontière moyenne : 1 


Algorithme : Approfondissement itératif (31 de profondeur) 

Temps moyen (s) : 34,94 

Nombre d’état exploré moyen : 831815 

Taille de la file frontière moyenne : 13 



Bien que les temps moyens de la recherche par largeur et par profondeur pourraient indiquer que la recherche en profondeur est toujours meilleure, une façon plus nuancée de voir les choses serait de dire que la recherche en largeur est plus performante lorsqu’il y a moins d’étape à explorer et la recherche en profondeur est plus performante lorsqu’il y en a plus. Aussi, l’approfondissement itératif peut se montrer extrêmement rapide avec les solutions qui ont peu d’état à explorer (plus que par la recherche en largeur), mais pour cela il faut s’assurer d’avoir un petit cutoff qui permettra quand même de trouver la solution.
