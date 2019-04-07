# Linux Kernel

## 进程管理

内核将进程的列表存放在任务队列(`task list`)的双向链表中。linux 通过slab分配器分配task_struct的结构，这样达到对象复用和内存着色的的目的。早期的linux，task_struct结构在内核栈的尾端，为了方便定位。有了slab以后，只需要创建一个`thread_info`结构在栈中即可。

![thread_info](./pic/thread_info.png)

### 进程状态

 - task_running
 - task_interruptible
 - task_uninterruptible
 - task_traced
 - task_stopped

![task_status](./pic/task_status.png)

linux中所有进程都是init(pid=1)的进程的子进程，而且在task_struct中都有一个指向其父进程的指针，还有子进程的链表。可以通过这个继承体系，遍历系统中的所有进程。

### 进程的创建

一般的系统创建进程是在新的地址空间中创建进程->读入可执行文件->运行。Linux用另一种方法，即`fork + exec`。Linux的fork使用copy-on-write技术实现，fork时内核并不复制整个进程地址空间，而是让父子进程共享同一个拷贝，只有需要写入的时候，数据才会被复制，从而使各个进程拥有各自的拷贝。fork的实际开销就是`复制父进程的页表以及给子进程创建唯一的进程描述符`。

#### fork

调动关系： fork -> clone -> do_fork -> copy_process
1. 调用dup_task_struct创建新的内核栈，thread_info, task_struct与父进程相同
2. 检查创建进程后，进程数量没有超过限制
3. 子进程将task_struct的一些成员清零或者设为初始值
4. 状态设为task_uninterruptible，确保不会被调度运行
5. 更新task_struct的flag成员
6. 分配一个新的pid
7. 拷贝父进程打开的文件，信号处理函数，地址空间等
8. 返回一个指向子进程的指针

### 线程

从内核角度来说，并没有线程的概念，把线程当成进程来处理，只是和其他进程共享地址空间。创建线程时也是调用`clone`，制定的参数如下：
```c
// thead
clone(CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND, 0);
// fork
clone(SIGCHLD, 0);
// vfork
clone(CLONE_VFORK | CLONE_VM | SIGCHLD, 0);
```
其实和fork差不多，知识他们共享地址空间，文件系统资源，文件描述符和信号处理程序。

## 进程调度

### 优先级

linux调度有优先级的概念，第一种时nice值，nice值指的是对其他进程的友好程度，nice值越高，调度的时间就越短。nice值可以代表时间片的比例或者绝对时间值（有负值）。另一种是实时优先级，可配置，实时进程优先级高于普通进程。

### 时间片

linux的时间片不是固定的，IO消耗型的进程希望获得更短的时间片，有利于请求的响应，处理器消耗型的进程希望获得长的时间片，有利于他们的cache命中。CFS调度器是将处理器的使用比例划分给了进程，时间片是和系统负载有关的，比例会受nice值的影响，高nice值进程权重低，丧失一部分处理器使用比。

linux系统是抢占式的，是否抢占取决于优先级和时间片。CFS的抢占时机取决于新的可运行程序消耗了多少处理器的使用比，如果消耗的使用比比当前进程小（也就是它被运行的少了）则抢占，否则推迟。

### UNIX调度的问题

1. nice单位值映射到处理器绝对时间是有缺陷的，假设0对应100ms,则+20对应5ms,这样，如果是两个低nice值的进程的调度，每个5ms就有一次调度，代价高。
2. nice 0,1是100ms和95ms，但是18,19却是10ms和5ms，比例失调。

### CFS公平调度

主要思想是让每个进程都能获得处理器调度的1/n的时间。

CFS允许每个进程运行一段时间，循环轮转，选择最少运行的进程作为下一个可运行的进程，将nice值作为一个运行权重（只和nice的相对值有关），不直接和时间片挂钩。CFS中每个进程最小运行时间片称为粒度，默认是1ms，轮转所有进程的时间段就是目标延迟时间。

### Linux调度实现

#### 时间记账

调度器实体结构作为成员变量，嵌入在进程描述符struct task_sturct中。`vruntime`是一个加权的运行时间，和定时器节拍无关，（可以理解为运行的进度？？），使用该变量来记录一个程序到底运行的多长时间以及还要运行多久。完美的任务调度中，vruntime应该是一致的，所以linux在调度的时候，选择最小vruntime的任务来运行。

CFS使用`红黑树`来组织可运行进程队列，可以迅速找到最小的vruntime值。