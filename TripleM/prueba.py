

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ("Fecha","Codigo", "Nombre", "Costo USD", "Costo CUP", "Precio", "Moneda", "Cantidad", "Cliente"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Codigo", width = 75, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo USD", width = 100, anchor="center")
        self.tabla.column("Costo CUP", width = 100, anchor="center")
        self.tabla.column("Precio", width = 75, anchor="center")
        self.tabla.column("Moneda", width = 75, anchor="center")
        self.tabla.column("Cantidad", width = 75, anchor="center")
        self.tabla.column("Cliente", width = 200, anchor="center")

        self.tabla.place(x = 100, y = 300)        
        self.tabla.config(height = 11)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Codigo", text = "Codigo", anchor="center")
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla.heading("Costo USD", text = "Costo USD", anchor="center")
        self.tabla.heading("Costo CUP", text = "Costo CUP", anchor="center")
        self.tabla.heading("Precio", text = "Precio", anchor="center")
        self.tabla.heading("Moneda", text = "Moneda", anchor="center")
        self.tabla.heading("Cantidad", text = "Cantidad", anchor="center")
        self.tabla.heading("Cliente", text = "Cliente", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        # ahora la posibilidad de eliminar el pago con doble click
        def eliminar_venta(event): 
            global id_venta
            global nombre_venta
            global codigo_venta
            global cantidad_venta

            # vamos a capturar el id del regalo que vamos a eliminar
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_venta = self.tabla.item(item, "text")  
                codigo_venta = self.tabla.item(item, "values")[1] 
                nombre_venta = self.tabla.item(item, "values")[2] 
                cantidad_venta = self.tabla.item(item, "values")[7]  

            conf = messagebox.askokcancel("Confirmar","Se va a cancelar esta venta") 
            if conf:
                # primero debemos devolver la venta al almacen
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
                        )
                    cursor = conn.cursor()               

                    sql = f""" UPDATE `productos` SET `Cantidad`= `Cantidad` + '{cantidad_venta}' WHERE `Codigo` = "{codigo_venta}"; """
                    cursor.execute(sql)
                    conn.commit()                

                except:
                    error = messagebox.showerror("Error","No se pudo devolver el producto al almacen")  

                # eliminamos la venta de la base de datos
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `salidas` WHERE `Id` = "{id_venta}" """
                    cursor.execute(sql)
                    conn.commit()
                    
                    llenar_tabla(True)

                except:
                    error = messagebox.showerror("Error","No se pudo borrar el regalo de la base de datos") 

        self.tabla.bind("<Double-1>", eliminar_venta)

        def llenar_tabla(event):
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "triplem",
                    password = "123456",
                    database = "triplem"
                    )
                cursor = conn.cursor()

                if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                    sql = f""" SELECT * FROM salidas WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' """

                else:
                    sql = f""" SELECT * FROM salidas WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """

                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],index[7],index[8],index[9],))  

            except:
                error = messagebox.showerror("Error","No se pudo actualizar la tabla")


        


        self.label_buscador = CTkLabel(self,text="---------- Buscador ----------")
        self.label_buscador.place(x=600,y=50)

        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...")
        self.texto_buscador_codigo.place(x=600,y=90)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...")
        self.texto_buscador_nombre.place(x=600,y=130) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla )

        llenar_tabla(True)



# **********************************************************************************
# ************************************  Almacen ************************************
# **********************************************************************************

class Almacen(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Almacen")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/TripleM/imagenes funcionamiento/triplem_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo Usd", "Cantidad", "Categoria"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre", width = 200)
        self.tabla.column("Costo Usd", width = 100)
        self.tabla.column("Cantidad", width = 100)
        self.tabla.column("Categoria", width = 100)

        self.tabla.place(x = 100, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo Usd", text = "Costo Usd")
        self.tabla.heading("Cantidad", text = "Cantidad")
        self.tabla.heading("Categoria", text = "Categoria")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "triplem",
                password = "123456",
                database = "triplem"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM productos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%'; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],))         

        # vamos a hacer un buscador 

        self.label_buscador = CTkLabel(self,text="------------------------------ Buscador ------------------------------")
        self.label_buscador.place(x=630,y=80)


        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...")
        self.texto_buscador_codigo.place(x=610,y=120)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...")
        self.texto_buscador_nombre.place(x=770,y=120) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla) 

        def doble_click(event):
            global codigo_almacen
            global nombre_almacen
            # vamos a capturar el codigo del producto
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                codigo_almacen = self.tabla.item(item, "text") 
                nombre_almacen = self.tabla.item(item, "values")[0]


            # vamos a crear la ventana modal
            temp = CTkToplevel()
            temp.title("Selección") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 200
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"200x200+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/TripleM/imagenes funcionamiento/triplem_icono.ico'))  

            def modificar():
                root = CTkToplevel()
                root.title("Modificar") 
                htotal = root.winfo_screenheight()
                wtotal = root.winfo_screenwidth()
                wventana = 1000
                hventana = 600
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                root.geometry(f"+{posx}+{posy}")
                root.geometry("1000x600") 
                root.lift()
                root.attributes('-topmost', True)
                root.after(200, lambda: root.attributes('-topmost', False)) 
                root.after(250, lambda: root.iconbitmap('D:/TripleM/imagenes funcionamiento/triplem_icono.ico')) 

                # ************************** Labels *************************        

                root.label_codigo = CTkLabel(root,text="Codigo:", font=("Times New Roman",16))
                root.label_codigo.place(x = 630, y = 70)   

                root.texto_codigo = CTkEntry(root)
                root.texto_codigo.place(x = 750, y = 70)     

                root.label_nombre = CTkLabel(root,text="Nombre:", font=("Times New Roman",16))
                root.label_nombre.place(x = 630, y = 110) 
                
                root.texto_nombre = CTkEntry(root)
                root.texto_nombre.place(x = 750, y = 110)       

                root.label_costo_usd = CTkLabel(root,text="Costo Lote Usd:", font=("Times New Roman",16))
                root.label_costo_usd.place(x = 630, y = 150)  

                root.texto_costo_usd = CTkEntry(root)
                root.texto_costo_usd.place(x = 750, y = 150) 

                def cambio():
                    vent = CTkToplevel()
                    vent.title("Cambio de Moneda") 
                    htotal = vent.winfo_screenheight()
                    wtotal = vent.winfo_screenwidth()
                    wventana = 300
                    hventana = 300
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    vent.geometry(f"+{posx}+{posy}")
                    vent.lift()
                    vent.attributes('-topmost', True)
                    vent.after(200, lambda: vent.attributes('-topmost', False)) 
                    vent.after(250, lambda: vent.iconbitmap('D:/TripleM/imagenes funcionamiento/triplem_icono.ico')) 

                    tar1 = 0           
                    tar2 = 0           
                    tar3 = 0 

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT * FROM `tarifas`;"""
                    cursor.execute(sql)
                    for index in cursor:
                        tar1 = index[0]
                        tar2 = index[1]
                        tar3 = index[2]

                    tarifa = f"Tarifa:  1USD = {tar1}CUP,  1EUR = {tar2}CUP, 1EUR = {tar3}CUP"                      

                    vent.label_tarifa = CTkLabel(vent,text=tarifa, font=("Times New Roman",16))
                    vent.label_tarifa.pack(pady=10)

                    vent.texto_cup = CTkEntry(vent, placeholder_text="CUP ...")
                    vent.texto_cup.pack(pady=5)

                    vent.texto_eur = CTkEntry(vent, placeholder_text="EUR ...")
                    vent.texto_eur.pack(pady=5)

                    def cambiar():
                        if vent.texto_cup.get() == "" and vent.texto_eur.get() == "":
                            error = messagebox.showerror("Error", "Debes escribir en algun campo la cantidad a cambiar")

                        elif vent.texto_cup.get() != "" and vent.texto_eur.get() != "":
                            error = messagebox.showerror("Error", "Debes escribir solo en un campo, no en ambos")

                        else:
                            if vent.texto_cup.get() != "":
                                root.texto_costo_usd.delete(0,END)
                                resultado = round(float(vent.texto_cup.get())/tar1,2)
                                root.texto_costo_usd.insert(0,resultado)
                                vent.destroy()

                            else:
                                root.texto_costo_usd.delete(0,END)
                                resultado = round(float(vent.texto_eur.get())*tar3,2)
                                root.texto_costo_usd.insert(0,resultado)
                                vent.destroy()


                    vent.btn_cambiar = CTkButton(vent, text="Cambiar", command=cambiar)
                    vent.btn_cambiar.pack(pady=10)           

                root.btn_cambio = CTkButton(root,text="...", width=30,command=cambio)      
                root.btn_cambio.place(x = 900, y = 150)  

                root.label_cantidad = CTkLabel(root,text="Cantidad:", font=("Times New Roman",16))
                root.label_cantidad.place(x = 630, y = 190)  

                root.texto_cantidad = CTkEntry(root)
                root.texto_cantidad.place(x = 750, y = 190)                 

                root.label_categoria = CTkLabel(root,text="Categoria:", font=("Times New Roman",16))
                root.label_categoria.place(x = 630, y = 230)  

                categorias = []
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "triplem",
                    password = "123456",
                    database = "triplem"
                    )
                cursor = conn.cursor()

                sql = """SELECT * FROM `categorias`;"""
                cursor.execute(sql)
                for index in cursor:
                    categorias.append(index[0])

                root.texto_categoria = CTkComboBox(root, values=categorias)
                root.texto_categoria.set("...")
                root.texto_categoria.place(x = 750, y = 230)

                # vamos a llenar los campos con la info que ya existe en la base de datos
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "triplem",
                    password = "123456",
                    database = "triplem"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `productos` WHERE `Codigo` = "{codigo_almacen}" """
                cursor.execute(sql)
                for index in cursor:
                    root.texto_codigo.insert(0,index[0])                     
                    root.texto_nombre.insert(0,index[1]) 
                    root.texto_costo_usd.insert(0,index[2]*index[3])
                    root.texto_cantidad.insert(0,index[3])                    
                    root.texto_categoria.set(index[4])


                def modificar_producto():
                    try:
                        conf = messagebox.askokcancel("Confirmar","Vamos a modificar el producto en la base de datos")
                        if conf:
                            # modificar el producto en la bd 
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "triplem",
                                password = "123456",
                                database = "triplem"
                                )
                            cursor = conn.cursor()                    

                            sql = f""" UPDATE `productos` SET `Codigo`='{root.texto_codigo.get()}',`Nombre`='{root.texto_nombre.get()}',`CostoUsd`='{float(root.texto_costo_usd.get())/float(root.texto_cantidad.get())}',`Cantidad`='{root.texto_cantidad.get()}',`Categoria`='{root.texto_categoria.get()}' WHERE `Codigo` = "{codigo_almacen}"; """
                            cursor.execute(sql)
                            conn.commit()

                            completado = messagebox.showinfo("Completado","Se modifico el producto")

                            llenar_tabla(True)
                            root.destroy()

                    except:
                        error = messagebox.showerror("Error","No se ha podido modificar el producto")

                root.btn_modificar = CTkButton(root,text="Modificar",command=modificar_producto, width = 150, height = 40)
                root.btn_modificar.place(x=650 ,y=500 )

            temp.btn_modificar = CTkButton(temp,text="Modificar", command=modificar)
            temp.btn_modificar.pack(pady=20)   

            def eliminar():
                string = f"Vamos a eliminar el producto: {nombre_almacen}"
                conf = messagebox.askokcancel("Confirmar",string)
                if conf:
                    try:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "triplem",
                            password = "123456",
                            database = "triplem"
                            )
                        cursor = conn.cursor()

                        sql = f""" DELETE FROM `productos` WHERE `Codigo` = "{codigo_almacen}" """
                        cursor.execute(sql)
                        conn.commit()
                    
                    except:
                        error = messagebox.showerror("Error","No se pudo eliminar el producto")

            temp.btn_eliminar = CTkButton(temp,text="Eliminar", command=eliminar)
            temp.btn_eliminar.pack(pady=20) 



        self.tabla.bind("<Double-1>", doble_click)  

        llenar_tabla(True)