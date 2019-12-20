
class Point:
    def __init__(self, x, y, user_data=""):
        self.x = x
        self.y = y
        self.userData = user_data

    def esigual(self, b):
        if b.x == self.x and b.y == self.y:
            return True
        return False

    def __str__(self):
        return str(self.x) + " " + str(self.y)


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        if self.x + self.w >= point.x >= self.x - self.w and self.y + self.h >= point.y >= self.y - self.h:
            return True
        return False

    def intersects(self, range):
        if range.x - range.w < self.x + self.w or range.y + range.h > self.y - self.h or range.y - range.h < self.y + self.h or range.x + range.w > self.x - self.w:
            return True
        return False

    def calcular_perimetro(self):
        return 4.0 * self.w + 4.0 * self.h

    def reorganizar_rectangulo(self,b):
        largo = 2.0 * self.w
        distancia_largo = 0
        if b.x < self.x - self.w:
            distancia_largo = b.x - (self.x - self.w)
            largo += ((self.x - self.w) - b.x)

        elif b.x > self.x + self.w:
            distancia_largo = b.x - (self.x + self.w)
            largo += (b.x - self.x + self.w)

        ancho = 2.0 * self.h
        distancia_ancho = 0
        if b.y < self.y - self.h:
            distancia_ancho = b.y - (self.y - self.h)
            ancho += ((self.y - self.h) - b.y)
        elif b.y > self.y + self.h:
            distancia_ancho = b.y - (self.y - self.h)
            ancho += (b.y - self.y + self.h)

        return Rectangle(self.x + (distancia_largo / 2), self.y + (distancia_ancho / 2), largo / 2, ancho / 2)

    def esigual(self, a):
        if a.x == self.x and a.y == self.y and a.w == self.w and a.h == self.h:
            return True
        return False

    def pasar_info(self, b):
        b.x = self.x
        b.y = self.y
        b.w = self.w
        b.h = self.h

    def contains_rectangle(self, a):
        if a.x - a.w < self.x - self.w:
            return False
        if a.x + a.w > self.x + self.w:
            return False
        if a.y - a.h < self.y - self.h:
            return False
        if a.y + a.h > self.y + self.h:
            return False
        return True


    def __str__(self):
        return str(self.x) + " " + str(self.y)

class Nodo:
    def __init__(self, B, parent=None):
        self.B = B
        self.child_nodes = []
        self.points = []
        self.parent_node = parent

    def isoverflow(self):
        if len(self.points) > self.B:
            return True
        return False

    def isroot(self):
        if self.parent_node:
            return True
        return False

    def isleaf(self):
        if len(self.child_nodes) == 0:
            return True
        return False

    def choose_subtree(self, b):
        pass
        a = None
        pos = 0
        c = Rectangle(0, 0, 0, 0)
        perimetro = 1e10
        for i in range(len(self.points)):
            if self.points[i].contains(b):
                pos = i
                return self.child_nodes[i], c, pos
            else:
                value = self.points[i].reorganizar_rectangle(b)
                new_perimetro = value.calcular_perimetro()
                if new_perimetro < perimetro:
                    pos = i
                    value.pasar_info(c)
                    perimetro = new_perimetro
                    a = self.child_nodes[i]
        return a, c, pos


def sortX(val):
    return val.x

def sortY(val):
    return val.y

class Cola:
    def __init__(self):
        self.items = []

    def estaVacia(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def avanzar(self):
        return self.items.pop(0)

    def tamano(self):
        return len(self.items)

    def front(self):
        return self.items[0]

class Rtree:
    def __init__(self, B):
        self.capacidad = B
        self.root = Nodo(B)


    def generar_graphviz(self):
        texto1 = open("arbol.dot")
        texto1.close()

        texto = open("arbol.dot")
        texto.write("digraph g {\n")
        texto.write("node [shape = record,height=.1];\n")
        values = Cola()
        padres = Cola()
        cantidad = Cola()
        values.push(self.root)
        nombre = "e"
        estado = 0
        node = 0
        helper = 0
        while not values.estaVacia():
            avan = not padres.estaVacia()
            aux = values.front()
            values.avanzar()
            if aux.isleaf():
                texto.write("node"+str(node)+"[label = "+'"')
                node+=1
                for i in range(len(aux.puntos)):
                    texto.write("<f"+str(i)+"> |("+str(int(aux.puntos[i].x))+","+str(int(aux.puntos[i].y))+")|")
                texto.write('"')
                texto.write("];\n")

                if avan:
                    if helper == cantidad.front():
                        padres.avanzar()
                        cantidad.avanzar()
                        helper = 0

                    texto.write('"')
                    texto.write("node" + str(padres.front()))
                    texto.write('"')
                    texto.write(":f" + str(helper)+ "-> ")
                    texto.write('"')
                    texto.write("node" +str(node-1))
                    texto.write('"')
                    texto.write("\n")
                    helper+=1
            else:
                texto.write("node"+str(node)+"[label = ")
                node+=1
                texto.write('"')
                for i in range(len(aux.puntos)):
                    texto.write("<f"+str(i)+"> |"+nombre+str(estado)+"|")
                    estado+=1
                    values.push(aux.child_nodes[i])

                    texto.write('"')
                    texto.write("];\n")
                    if avan:
                        if helper == cantidad.front():
                            padres.avanzar()
                            cantidad.avanzar()
                            helper = 0

                        texto.write('"')
                        texto.write("node" + str(padres.front()))
                        texto.write('"')
                        texto.write(":f"'"'+ str(helper) + "-> ")
                        texto.write('"')
                        texto.write("node" + str(node-1))
                        texto.write('"')
                        texto.write("\n")
                        helper+=1
                    padres.push(node-1)
                    cantidad.push(len(aux.points))

        texto.write("}\n")
        texto.close()


    def obtener_rectangulo_puntos(self,a, estado):
        answer = Rectangle(0, 0, 0, 0);
        if estado:
            answer.w = (a[a.size() - 1].x - a[0].x) / float(2.0)
            answer.x = a[a.size() - 1].x - answer.w
            a.sort(key=sortY)
            answer.h = (a[a.size() - 1].y - a[0].y) / float(2.0)
            answer.y = a[a.size() - 1].y - answer.h

        else:

            answer.h = (a[a.size() - 1].y - a[0].y) / float(2.0)
            answer.y = a[a.size() - 1].y - answer.h
            a.sort(key=sortX)
            answer.w = (a[a.size() - 1].x - a[0].x) / float(2.0)
            answer.x = a[a.size() - 1].x - answer.w

        return answer

    def evaluar_leaf(self, valores, data1, data2, rectangulo1, rectangulo2, estado):
        valor_min = int(0.4 * self.capacidad)
        perimetro_minimo = 1e10 if rectangulo1.calcular_perimetro() + rectangulo2.calcular_perimetro() == 0 else rectangulo1.calcular_perimetro() + rectangulo2.calcular_perimetro()

        for i in range(valor_min,len(valores) - valor_min):
            a1 = valores[:i]
            a2 = valores[i:]
            prueba = self.obtener_rectangulo_puntos(a1[:], estado)
            prueba1 = self.obtener_rectangulo_puntos(a2[:], estado)
            p_prueba = prueba.calcular_perimetro()
            p_prueba1 = prueba1.calcular_perimetro()
            if p_prueba + p_prueba1 < perimetro_minimo:
                perimetro_minimo = p_prueba + p_prueba1
                prueba.pasar_info(rectangulo1)
                prueba1.pasar_info(rectangulo2)
                data1 = a1
                data2 = a2

    def split_leaf(self, a, best1, best2,ans1,ans2):
        a.sort(key= sortX)
        self.evaluar_leaf(a[:], best1.points, best2.points, ans1, ans2, True)
        a.sort(key=sortY)
        self.evaluar_leaf(a[:], best1.points, best2.points, ans1, ans2, False)

    def split_nodos(self):
        return 0

    def updateMBR(self, hijo, padre):
        sfsd = 0

    def handle_overflow(self, u):
        best1 = Nodo(u.capacidad)
        best2 = Nodo(u.capacidad)
        ans = Rectangle(0, 0, 0, 0)
        ans1= Rectangle(0, 0, 0, 0)

        if u.isleaf():
            self.split_leaf(u.points, best1, best2, ans, ans1)
        else:
            self.split_nodos()

        if u.isroot():
            new_root = Nodo(u.capacidad)
            new_root.points.append(ans)
            new_root.points.append(ans1)
            new_root.child_nodes.append(best1)
            best1.padre = new_root
            new_root.child_nodes.append(best2)
            best2.padre = new_root
            aux = self.root
            self.root = new_root
            del aux
        else:
            padre_u = u.padre
            self.updateMBR(u, padre_u)
            if padre_u.isoverflow():
                self.handle_overflow(padre_u)

    def insert(self, p):
        return self.insert2(self.root, p)

    def insert2(self, u, p):
        if u.isleaf():
            u.data.append(p)
            if u.is_overflow(u):
                self.handle_overflow(u)
        else:
            v = u.choose_subtree(u, p)
            self.insert2(v, p)




B = 3
extra = Rtree(B)

