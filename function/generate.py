charts = []
idx = 0


def generate_all(param):
    """
    param : {
        "id": gen_id(),
        "about": form.about.data,
        "path": path,
        "time": datetime.now()
    }
    """
    import matplotlib.pyplot as plt
    import csv

    def DictToArray(Dict):
        keys = []
        values = []
        for k in Dict.keys():
            if Dict[k] == 0:
                continue
            keys.append(k)
            values.append(Dict[k])
        return keys, values

    def PieChart(title, labels, data):
        global idx

        if len(labels) > 10:
            return

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title(title, fontsize=18)

        ax.pie(data,
               labels=labels,
               autopct='%.1f%%',
               wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})

    def BarChart(title, labels, data):
        global idx

        if len(labels) > 10:
            return

        x = [i + 1 for i in range(len(labels))]

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title(title, fontsize=18)

        ax.bar(x,
               data,
               tick_label=labels,
               width=0.5)

    def LineGraph(x_name, x, y_name, y):
        global idx

        data = [[x[i], y[i]] for i in range(len(x))]
        data.sort()
        for i in range(len(x)):
            x[i] = data[i][0]
            y[i] = data[i][1]
            if i > 0 and x[i] == x[i - 1]:
                return

        # fig, ax = plt.subplots(figsize=(6, 6))
        plt.figure(idx)
        idx += 1

        plt.xlim(x[0], x[-1])
        plt.ylim(min(y), max(y))
        plt.plot(x, y)
        plt.grid()
        plt.xlabel(x_name, fontsize=12)
        plt.ylabel(y_name, fontsize=12)

    def ScatterGraph(x_name, x, y_name, y):
        global idx

        plt.figure(idx)
        idx += 1

        plt.scatter(x, y, alpha=0.5)
        plt.grid()
        plt.xlabel(x_name, fontsize=12)
        plt.ylabel(y_name, fontsize=12)

    with open(param['path'], newline='') as csvfile:
        rows = list(csv.reader(csvfile))

        labels = []
        types = []
        for l in rows[0]:
            labels.append(l)
            types.append(1)

        Dict = {}
        for i in range(len(labels)):
            Dict[labels[i]] = {}

        cols = [[] for _ in range(len(labels))]
        for i in range(1, len(rows)):
            for j in range(len(labels)):
                if not (rows[i][j] in Dict[labels[j]]):
                    Dict[labels[j]][rows[i][j]] = 0
                Dict[labels[j]][rows[i][j]] += 1
                cols[j].append(rows[i][j])
                try:
                    int(rows[i][j])
                except:
                    types[j] = 0

        for i in range(len(types)):
            if types[i] == 1:
                for j in range(len(cols[i])):
                    cols[i][j] = int(cols[i][j])

        for i in range(len(labels)):
            k = labels[i]
            L, D = DictToArray(Dict[k])
            if types[i] <= 1:
                PieChart(k, L, D)
                plt.savefig('static/' + param['id'] + '-1.jpg')
                BarChart(k, L, D)
                plt.savefig('static/' + param['id'] + '-2.jpg')

        for i in range(len(labels)):
            if types[i] == 1:
                for j in range(i + 1, len(labels)):
                    if types[j] == 1:
                        LineGraph(labels[i], cols[i], labels[j], cols[j])
                        plt.savefig('static/' + param['id'] + '-3.jpg')
                        ScatterGraph(labels[i], cols[i], labels[j], cols[j])
                        plt.savefig('static/' + param['id'] + '-4.jpg')
