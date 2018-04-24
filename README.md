
# Cascade Influence

This repository contains:

 - The scripts to estimate user influence from Twitter information cascades (i.e. Cas.In);
 - A small dataset of 20 cascades for testing Cas.In;
 - A hands-on tutorial to walk you through running Cas.In on real cascades.

### Citation
The algorithm was introduced in the paper:

Rizoiu, M.-A., Graham, T., Zhang, R., Zhang, Y., Ackland, R., & Xie, L. (2018). **#DebateNight: The Role and Influence of Socialbots on Twitter During the 1st 2016 U.S. Presidential Debate**. In *Proc. International AAAI Conference on Web and Social Media (ICWSM ’18)* (pp. 1–10). Stanford, CA, USA.  
[pdf at arxiv with supplementary material](https://arxiv.org/abs/1802.09808)

**Bibtex**
```
@article{rizoiu2018debatenight,
  title={#DebateNight: The Role and Influence of Socialbots on Twitter During the 1st US Presidential Debate},
  author={Rizoiu, Marian-Andrei and Graham, Timothy and Zhang, Rui and Zhang, Yifei and Ackland, Robert and Xie, Lexing},
  journal={arXiv preprint arXiv:1802.09808},
  year={2018}
}
```

### License
Both dataset and code are distributed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license, a copy of which can be obtained following this link. If you require a different license, please contact [Yifei Zhang](mailto:yifeiacc@gmail.com), [Marian-Andrei Rizoiu](mailto:Marian-Andrei@rizoiu.eu) or [Lexing Xie](mailto:Lexing.Xie@anu.edu.au).

# How to run Cas.In in a terminal:

### Required packages:

  - python3
  - numpy
  - pandas
    
### Arguments of Cas.In:

*--cascade_path* : the path of cascade file (see the format here below). 

*--time_decay* : the coefficient value of time decay (hyperparameter $r$ in the paper). **Default**:-0.000068

*--save2csv* : save result to csv file. **Default**: False

### Command:
```bash
cd scripts
python3 influence.py --cascade_path path/to/file
```

# File format and toy dataset

### Dataset
We provide a toy dataset -- dubbed SMH -- for testing Cas.In.
It was collected in 2017 by following the Twitter handle of the Sydney Morning Herald newspaper (tweets and retweets mentioning SMH or linking to an article from SMH). 

The data contains 20 cascades (one file per cascade).
We annonymized the `user_id` (as per Twitter's ToS) by mapping original values to a sequence from 0 to n, while preserving the identity of users across cascades.

### The format cascade files:
 - A csv file with 3 columns (`time`, `magnitude`, `user_id`), where each row is a tweet in the cascade:
    - `time` represents the timestamp of tweet -- the first tweet is always at time zero, for the following retweets it shows the offset in seconds from the initial tweet;
    - `magnitude` is the local influence of the user (here the number of followers);
    - `user_id` the id of the user emitting the tweet (here annonymized).
 - The rows in the file (i.e. the tweets) are sorted by the timestamp;
 
eg:
```
time,magnitude,user_id 
0,4674,"0"
321,1327,"1"
339,976,"2"
383,477,"3"
699,1209,"4"
824,119,"5"
835,1408,"6"
1049,896,"7"
```

# Cascade influence tutorial

Next, we drive you through using Cas.In for estimating user influence starting from a single cascade.

###  Preliminary
We need to first load all required packages of cascade influence.


```python
cd scripts
```
   
```python
import pandas as pd
import numpy as np
from casIn.user_influence import P,influence
```

## Compute influence in one cascade

###  Read data
Load the first cascade in the SMH toy dataset:


```python
cascade = pd.read_csv("../data/SMH/SMH-cascade-0.csv")
cascade.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>time</th>
      <th>magnitude</th>
      <th>user_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>991</td>
      <td>419</td>
    </tr>
    <tr>
      <th>1</th>
      <td>127</td>
      <td>1352</td>
      <td>658</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2149</td>
      <td>2057</td>
      <td>264</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2465</td>
      <td>1155</td>
      <td>1016</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2485</td>
      <td>1917</td>
      <td>790</td>
    </tr>
  </tbody>
</table>
</div>



###  Compute matrix P

We first need to compute the probabilities ![$p_{ij}$](http://latex.codecogs.com/gif.latex?%24p_%7Bij%7D%24), where ![$p_{ij}$](http://latex.codecogs.com/gif.latex?%24p_%7Bij%7D%24) is the probability that ![$j^{th}$](http://latex.codecogs.com/gif.latex?%24j%5E%7Bth%7D%24) tweet is a direct retweet of the ![$i^{th}$](http://latex.codecogs.com/gif.latex?%24i%5E%7Bth%7D%24) (see the paper for more details).
We need to specify the hyper-parameter ![$r$](http://latex.codecogs.com/gif.latex?%24r%24),  the time decay coefficient. 
Here we choose ![$r = -0.000068$](http://latex.codecogs.com/gif.latex?%24r%20%3D%20-0.000068%24).


```python
p_ij = P(cascade,r = -0.000068)
```

###  Compute user influence and matrix M
The function `influence()` will return an array of influences for each user and the matrix ![$M = m_{ij}$](http://latex.codecogs.com/gif.latex?%24M%20%3D%20m_%7Bij%7D%24), where ![$m_{ij}$](http://latex.codecogs.com/gif.latex?%24m_%7Bij%7D%24) is the influence of the ![$i^{th}$](http://latex.codecogs.com/gif.latex?%24i%5E%7Bth%7D%24) tweet of the ![$j^{th}$](http://latex.codecogs.com/gif.latex?%24j%5E%7Bth%7D%24) tweet (direct and indirect).


```python
inf, m_ij = influence(p_ij)
```

###  Link influence with user_id

Now, we add the computed user influence back to the pandas data structure.


```python
cascade["influence"] = pd.Series(inf)
cascade.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>time</th>
      <th>magnitude</th>
      <th>user_id</th>
      <th>influence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>991</td>
      <td>419</td>
      <td>60.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>127</td>
      <td>1352</td>
      <td>658</td>
      <td>34.590370</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2149</td>
      <td>2057</td>
      <td>264</td>
      <td>29.656122</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2465</td>
      <td>1155</td>
      <td>1016</td>
      <td>13.535845</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2485</td>
      <td>1917</td>
      <td>790</td>
      <td>15.913873</td>
    </tr>
  </tbody>
</table>
</div>



## Compute influence over multiple cascades
### Load function
The function *casIn()* compute influence in one cascade, which basically contain all the steps described above


```python
from casIn.user_influence import casIn
influence = casIn(cascade_path="../data/SMH/SMH-cascade-0.csv",time_decay=-0.000068)
influence.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>time</th>
      <th>magnitude</th>
      <th>user_id</th>
      <th>influence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>991</td>
      <td>419</td>
      <td>60.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>127</td>
      <td>1352</td>
      <td>658</td>
      <td>34.590370</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2149</td>
      <td>2057</td>
      <td>264</td>
      <td>29.656122</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2465</td>
      <td>1155</td>
      <td>1016</td>
      <td>13.535845</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2485</td>
      <td>1917</td>
      <td>790</td>
      <td>15.913873</td>
    </tr>
  </tbody>
</table>
</div>



### Load multiple cascades

The SMH toy dataset contains 20 cascades for testing out Cas.In.
Let's load all of them:


```python
cascades = []
for i in range(20):
    inf = casIn(cascade_path="../data/SMH/SMH-cascade-%d.csv" % i,time_decay=-0.000068)
    cascades.append(inf)
cascades = pd.concat(cascades)
```

### Compute user influence in multiple cascades

The influence of a user is by definition the mean influence of the tweets they emit.
We compute the user influence as follows:


```python
result = cascades.groupby("user_id").agg({"influence" : "mean"})
result.sort_values("influence",ascending=False).head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>influence</th>
    </tr>
    <tr>
      <th>user_id</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>734</th>
      <td>214.000000</td>
    </tr>
    <tr>
      <th>1225</th>
      <td>205.000000</td>
    </tr>
    <tr>
      <th>755</th>
      <td>190.554571</td>
    </tr>
    <tr>
      <th>60</th>
      <td>189.557461</td>
    </tr>
    <tr>
      <th>581</th>
      <td>141.033129</td>
    </tr>
  </tbody>
</table>
</div>


