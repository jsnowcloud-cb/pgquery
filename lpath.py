input_csv = """0XCEFC23CA9DEE424229518BE3CC184A9EE96E6059
0X78BBABE8DCFDCDA4EBCD19E84C2E7A9FCCE1E793
"""

starts = input_csv.toLowerCase().split("\n")

n = g.V().count().next()
vmap = [:]
vvmap = [:]
g.V().id().eachWithIndex{n, i -> vmap[n] = i; vvmap[i] = n}

class PathSet {
  List<int[]> path
}
v = new PathSet[n]
for (int i = 0; i < n; i++) {
  v[i] = new PathSet()
  v[i].path = new ArrayList<int[]>()
}

for (int i = 0; i < starts.size(); i++) {
  def rid = RecordId.from("node:::" + starts[i])
  def x = vmap[rid]
  if (x != null) {
    v[x].path.add([x])
  }
}

def extend(List<Integer> path, int v) {
  if (path.contains(v)) {
    return []
  } else {
    def newPath = path.clone()
    newPath.add(v)
    return newPath
  }
}

ee = g.E().order().by('tvalue').toList()
for (int i = 0; i < ee.size(); i++) {
  def start = vmap[ee[i].getOutVertex().id()]
  def end = vmap[ee[i].getInVertex().id()]

  for (int j = 0; j < v[start].path.size(); j++) {
    def p = v[start].path[j]
    def p2 = extend(p, end)
    if (p2.size() > 0) {
      v[end].path.add(p2)
    }
    v[end].path = v[end].path.stream().sorted { a, b -> b.size() <=> a.size() ?: a.hashCode() <=> b.hashCode() }.limit(10).collect(java.util.stream.Collectors.toList())
  }
}

a = []
b = []
for (int i = 0; i < n; i++) {
  def l = v[i].path[0]?.size() ?: 0;
  if (a.size() < l) a = v[i].path[0]
  b.add(l)
}

aa = []
for (int i = 0; i < a.size(); i++) {
  aa.add(vvmap[a[i]])
}

aa
