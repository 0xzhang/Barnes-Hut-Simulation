# Barnes-Hut Simulation

## 作业来源
N-body（多体）问题用来描述，给定每个物体当前的位置和速度，预测一群物体在相互引力作用下的运动轨迹。N-body问题最早在牛顿研究木星和其卫星的运动时提出。在天文领域中有广泛应用。

N-body问题的求解算法有很多相关研究，也常常作为并行算法学习的典型案例。朴素的精确算法是计算N个粒子中两两之间（Particle-Particle）的引力，这种方法具有 $$ O(N^2) $$ 的时间复杂度。真实的天体模拟中往往需要模拟数以亿计的粒子，对于这种规模的问题， $$ O(N^2) $$的时间复杂度将使问题不可求解。为此，天文学家创造了很多近似方法用于求解N-body问题，比如基于树的方法（Barnes-Hut algorithm, [Barnes and Hut 1986](https://anaroxanapop.github.io/behalf/#Citations)）和粒子网格算法（[Darden et al. 1993](https://anaroxanapop.github.io/behalf/#Citations)）等。

在我的笔记本电脑上，示例程序`nbody.py`中的粒子设置到3000以上时，就无法达到60FPS了。想尝试用taichi实现BH算法求解N-body问题，使用近似算法进行加速。实现过程中，发现并不能达到理想的效果，比如每次迭代中构造Quadtree目前只能是串行的，而且原生Python中递归的遍历树效率较低，可能也还没掌握好Advanced data layout:cry:。

示例程序`nbody.py`全部使用field进行初始化、计算是非常快的，为了可以和使用了BH算法的程序`nbody_barnes_hut.py比较`，使用相同的粒子类重新构造 $$ O(N^2) $$的计算程序`nbody_naive.py`，使用BH算法还是有加速效果的。

## 运行方式
#### 运行环境
```shell
[Taichi] version 0.8.3, llvm 10.0.0, commit 021af5d2, win, python 3.8.10
```

#### 运行
```shell
$ python nbody_naive.py
$ python nbody_barnes_hut.py
```

## 效果展示
> N = 100
>
> galaxy_size = 0.2

<a href="nbody_naive.gif"><img src="imgs/nbody_naive.gif" height=512px title="nbody_naive"></a>

<a href="nbody_barnes_hut.gif"><img src="imgs/nbody_barnes_hut.gif" height=512px title="nbody_barnes_hut"></a>

## 整体结构
```shell
├── LICENSE
├── requirements.txt
├── imgs
│   ├── nbody_quadtree.gif
│   └── nbody_naive.gif
├── body.py	# 粒子类
├── quadtree.py	# Quadtree类
├── nbody_barnes_hut.py	# 使用BH算法的主程序
├── nbody_naive.py	# 使用朴素算法的主程序
└── README.md
```

## 实现细节
## 参考资料

1. Barnes, J., & Hut, P. (1986). A hierarchical O(N log N) force-calculation algorithm. Nature, 324(6096), 446–449. doi:10.1038/324446a0
2. [battaglia-michael/N-body-Galaxy-Simulation: Simulate an N-body galaxy using a Barnes-Hut recursive tree algorithm (github.com)](https://github.com/battaglia-michael/N-body-Galaxy-Simulation)
3. [yboetz/nbody_bhtree: N-body simulation using a Barnes-Hut tree algorithm (github.com)](https://github.com/yboetz/nbody_bhtree)
4. [Barnes-Hut Algorithm for CS205 (anaroxanapop.github.io)](https://anaroxanapop.github.io/behalf/)
5. [The Barnes-Hut Approximation (jheer.github.io)](https://jheer.github.io/barnes-hut/)
6. [The Barnes-Hut Algorithm (arborjs.org)](http://arborjs.org/docs/barnes-hut)
7. [The Barnes-Hut Galaxy Simulator (beltoforion.de)](https://beltoforion.de/en/barnes-hut-galaxy-simulator/)
8. [Barnes-Hut Simulation, Prof. Viktor Kuncak, LARA – Lab for Automated Reasoning and Analysis - (epfl.ch)](https://lara.epfl.ch/w/parcon18/project4)
