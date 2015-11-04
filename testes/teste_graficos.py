# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 18:54:05 2015

@author: lucas
"""

import matplotlib.pyplot as plt


# The slices will be ordered and plotted counter-clockwise.
labels = 'Positivo', 'Negativo', 'Neutro'
sizes = [15, 30, 55]
colors = ['yellowgreen', 'lightcoral', 'silver']
explode = (0.1, 0, 0) # only "explode" the 1st slice (i.e. 'Hogs')

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')

plt.show()