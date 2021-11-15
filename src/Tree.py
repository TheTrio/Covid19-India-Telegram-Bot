from Node import Node

class Tree:
    def __init__(self):
        help = Node('help','This generates a detailed guide on all the commands available\. However, it can also be intimidating and new users are advised to use the query builder instead of typing commands on their own', command='/help')
        graph = Node('graph','This is used to generate graphs',command='/graph')
        update = Node('update', 'This updates you about the latest Covid19 numbers in India',command='/update')
        district = Node('district','This gives you information about the spread of Covid19 in your district',command='/district')
        factcheck = Node('factcheck', 'Searches across multiple fact checking websites and displays the top 3 results', command='/factcheck')
        daily = Node('daily', 'Use this if you want to plot a graph of the number of cases on each day')
        total = Node('total', 'Use this if you want to plot a graph of the cumulative cases')
        new = Node('new', 'Use this if you want to plot a graph of new cases')
        india = Node('India', 'Use this if you want to generate graphs of Indian States')
        world = Node('World', 'Use this if you want to generate graphs of different countries around the world')
        world.children = [new, total]
        india.children = [new,total]
        daily.children = [world,india]
        weekly = Node('weekly', 'Use this if you want to plot a graph of the 7 day moving average')
        bar = Node('bar', 'Use this if you want a bar chart')
        line = Node('line', 'Use this if you want a line chart')
        weekly.children = [bar, line]
        graph.children = [daily, weekly]
        self.children = [help, graph, update, district, factcheck]
