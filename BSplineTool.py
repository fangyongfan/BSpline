# 开曲线
import numpy as np
import matplotlib.pyplot as plt


def Nu(i, u, k, U):
    if k == 0:
        if u >= U[i] and u < U[i + 1]:
            return 1
        else:
            return 0
    else:
        a1 = (u - U[i])
        c1 = (U[i + k] - U[i])
        b1 = (U[i + k + 1] - u)
        d1 = (U[i + k + 1] - U[i + 1])
        if d1 < 0.0001:
            b1 = 0
            d1 = 1
        if c1 < 0.0001:
            a1 = 0
            c1 = 1
        nu = (a1 / c1) * Nu(i, u, k - 1, U) + (b1 / d1) * Nu(i + 1, u, k - 1, U)
        return nu


def generateCurvePoints(originPoints):
    #############################################################################################################
    # step1 参数初始化
    #############################################################################################################
    m = len(originPoints) - 1
    k = 3  # 代码只支持k=4次

    #############################################################################################################
    # step2 积累弦长
    #############################################################################################################
    L = 0
    l = [0] * m
    for i in range(0, m):
        l[i] = np.sqrt(
            (originPoints[i + 1][0] - originPoints[i][0]) ** 2 + (originPoints[i + 1][1] - originPoints[i][1]) ** 2)
        L += l[i]

    #############################################################################################################
    # step3 节点矢量
    #############################################################################################################
    U = [0] * (m + 1 + 2 * k)
    for i in range(0, k + 1):
        U[i] = 0
        U[i + m + k] = 1
    for i in range(k + 1, m + k):
        L2 = 0
        for j in range(0, i - k):
            L2 += l[j]
        U[i] = L2 / L
    print('U=', U)

    #############################################################################################################
    # step4 Delta，公式中的三角形的东西
    #############################################################################################################
    delta = [0] * (m + 2 * k)
    for i in range(0, m + 2 * k):
        delta[i] = U[i + 1] - U[i]
    print('Delta=', delta)

    #############################################################################################################
    # step5 系数矩阵的参数
    #############################################################################################################
    a = [0] * (m + 1)
    b = [0] * (m + 1)
    c = [0] * (m + 1)
    e = [0] * (m + 1)
    f = [0] * (m + 1)
    # 抛物线条件
    a[0] = 1 - delta[3] * delta[4] / ((delta[3] + delta[4]) ** 2)
    b[0] = delta[3] / (delta[3] + delta[4]) * (delta[4] / (delta[3] + delta[4]) - delta[3] / (delta[3] + delta[4] + delta[5]))
    c[0] = delta[3] * delta[3] / ((delta[3] + delta[4]) * (delta[3] + delta[4] + delta[5]))
    e[0] = 1 / 3 * (originPoints[0][0] + 2 * originPoints[1][0])
    f[0] = 1 / 3 * (originPoints[0][1] + 2 * originPoints[1][1])
    a[m] = -delta[m + 2] * delta[m + 2] / ((delta[m + 1] + delta[m + 2]) * (delta[m + 1] + delta[m + 1] + delta[m + 2]))
    b[m] = delta[m + 2] / (delta[m + 1] + delta[m + 2]) * (delta[m + 2] / (delta[m + 1] + delta[m + 1] + delta[m + 2]) - delta[m + 1] / (delta[m + 1] + delta[m + 2]))
    c[m] = delta[m + 1] * delta[m + 2] / ((delta[m + 1] + delta[m + 2]) ** 2) - 1
    e[m] = -1 / 3 * (originPoints[m][0] + 2 * originPoints[m - 1][0])
    f[m] = -1 / 3 * (originPoints[m][1] + 2 * originPoints[m - 1][1])

    for i in range(1, m):
        a[i] = delta[i + 3] ** 2 / (delta[i + 1] + delta[i + 2] + delta[i + 3])
        b[i] = delta[i + 3] * (delta[i + 1] + delta[i + 2]) / (delta[i + 1] + delta[i + 2] + delta[i + 3]) + delta[i + 2] * (delta[i + 3] + delta[i + 4]) / (delta[i + 2] + delta[i + 3] + delta[i + 4])
        c[i] = delta[i + 2] ** 2 / (delta[i + 2] + delta[i + 3] + delta[i + 4])
        e[i] = (delta[i + 2] + delta[i + 3]) * originPoints[i][0]
        f[i] = (delta[i + 2] + delta[i + 3]) * originPoints[i][1]
    print('a=', a)
    print('b=', b)
    print('c=', c)
    print('e=', e)
    print('f=', f)

    #############################################################################################################
    # step6 构造系数矩阵
    #############################################################################################################
    matrix = np.zeros((m + 1, m + 1))
    matrix[0][0] = a[0]
    matrix[0][1] = b[0]
    matrix[0][2] = c[0]
    matrix[m][m - 2] = a[m]
    matrix[m][m - 1] = b[m]
    matrix[m][m - 0] = c[m]
    for i in range(1, m):
        matrix[i][i - 1] = a[i]
        matrix[i][i + 0] = b[i]
        matrix[i][i + 1] = c[i]
    print('matrix=', matrix)

    # 求逆
    matrix_inv = np.linalg.inv(matrix)
    print('matrix_inv=', matrix_inv)
    # print('求逆结果',np.dot(matrix,matrix_inv))#验证求逆结果

    #############################################################################################################
    # step7 求控制点
    #############################################################################################################
    ctrl_xs = np.dot(matrix_inv, e)
    ctrl_ys = np.dot(matrix_inv, f)
    # 在最前面添加，第一个控制点和第一个型值点重合
    ctrl_xs = np.insert(ctrl_xs, 0, originPoints[0][0])
    ctrl_ys = np.insert(ctrl_ys, 0, originPoints[0][1])
    # 在最后面添加，最后一个控制点和最后一个型值点重合
    ctrl_xs = np.append(ctrl_xs, originPoints[m][0])
    ctrl_ys = np.append(ctrl_ys, originPoints[m][1])
    ctrlPoints = []
    for i in range(len(ctrl_xs)):
        ctrlPoints.append([ctrl_xs[i], ctrl_ys[i]])
    print('control points=', ctrlPoints)

    #############################################################################################################
    # step8 求插值点
    #############################################################################################################
    curvePoints = []
    i = 3
    u = 0
    while u < 1:
        tmp = [0, 0]
        if u > U[i + 1]:
            i += 1
        for k in range(4):
            t = [ctrlPoints[i - k][0], ctrlPoints[i - k][1]]
            t[0] *= Nu(i - k, u, 3, U)
            t[1] *= Nu(i - k, u, 3, U)
            tmp[0] += t[0]
            tmp[1] += t[1]
        curvePoints.append(tmp)
        # u += 0.01 #u可以自定义取值大小
        u+=1/m/20
    curvePoints.append([originPoints[m][0], originPoints[m][1]])

    #############################################################################################################
    # step9 返回控制点和插值点
    #############################################################################################################
    return ctrlPoints, curvePoints


if __name__ == '__main__':
    originPoints = [[1, 1], [2, 2], [3, 5], [4, 2], [4.5, 1.3], [5, 1], [7, 0.5], [8, -1.5]]
    # originPoints = [[1,1],[2,2],[3,5],[4,2],[4,1.5],[5,1],[7,0.5],[8,-1.5]]

    ctrlPoints, curvePoints = generateCurvePoints(originPoints)

    originPoints = np.array(originPoints)
    ctrlPoints = np.array(ctrlPoints)
    curvePoints = np.array(curvePoints)
    plt.figure()
    plt.plot(originPoints[:, 0], originPoints[:, 1], 'bo', label='Original Points')
    plt.plot(ctrlPoints[:, 0], ctrlPoints[:, 1], 'r^--', label='Control Points')
    plt.plot(curvePoints[:, 0], curvePoints[:, 1], 'g-', label='B-spline Curve')
    plt.legend()
    plt.title('B-spline Curve with Original Points')
    plt.show()
