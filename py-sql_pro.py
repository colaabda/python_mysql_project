import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

con=mysql.connector.connect(host='localhost', password='Home_oct23',user='root',database='restaurentdb')
if con.is_connected():print("srv_on")
cursor=con.cursor()

class bakery_offline_order():
#restaurentdb->resmenu

    def cake_choice(self):
        #self.menu={'black_forest':500,'red_velvate':600,'vanila':500,'chocolate':450}
        print("0.5kg & 1kg \n Enter cake size:");self.cake_size=float(input())
        #print("Prices of 1kg cake: \n black forest:500,red velvate:600,vanila:500,chocolate:450 \n Enter your choice" )
        self.cake_size=float(input())
        cursor.execute('select * from resmenu')
        self.prnt=cursor.fetchall()
        print(self.prnt)
        self.cake_pick=input();cursor.execute("select price from resmenu where item='"+self.cake_pick+"'")
        am=cursor.fetchall()
        for i in am:
            self.amount=int(''.join(map(str,i)))

        if self.cake_size==0.5:
            self.amount=self.amount//2
            print(self.amount)

    def addon_choice(self):
        cursor.execute('select * from add_on');prnt=cursor.fetchall()
        #self.add_ons={'candles':30,'baloons':50,'decoration':200}
        print("which service , you would like to add",prnt) #candles:30,baloons:50,decoration:200")
        self.addon_pick=input()

        print("Enter number of packets:")
        self.add_on_quantity=int(input())
        cursor.execute("select price from add_on where add_onitems='"+self.addon_pick+"'");val=cursor.fetchall()
        for i in val:
            rs=int(''.join(map(str,i)))
        self.amount +=  (rs*self.add_on_quantity)

    def homedelivery_choice(self):
        cursor.execute('select * from delivery')
        prnt=cursor.fetchall()
        #self.home_delivery={10:100,20:200}
        print("enter delivery range:",prnt)    #\n 10kmradius:100,20kmradius:200")
        self.distance=input()
        cursor.execute("select price from delivery where distance='"+self.distance+"'");val1=cursor.fetchall()
        for i in val1:
            res1=int(''.join(map(str,i)))
        self.amount+=res1           #home_delivery[i];print(self.amount)
        self.address=input("Enter Address")
                #print(amount)

    def orderid_generation(self):
        self.date_of_dispatch=int(input(print("Date of Delivery:")))
        self.name_on_cake=input(print("Name on cake"));self.name_on_cake=self.name_on_cake.upper()
        self.date_of_order=int(input(print("date of order")))
        self.order_id =self.date_of_dispatch + self.date_of_order

    def details_of_bill(self):
        #print("inter function data communication is pending")
        #print("Cake picked:",self.cake_pick,"Date of delivery:",self.date_of_dispatch,"Name on cake:",self.name_on_cake,
             # "Date of placing order:",self.date_of_order,"Order ID:",self.order_id,"Amount to be paid:",self.amount,"Adress:",self.address,
              #"Details of Addons:",self.addon_pick,"Details of addon quantity:",self.add_on_quantity,)
        #cursor=con.cursor()
        query="insert into orderdb value('{}',{},'{}',{},{},{},'{}','{}',{})".format(self.cake_pick,self.date_of_dispatch,self.name_on_cake,
                   self.date_of_order,self.order_id,self.amount,self.address,self.addon_pick,self.add_on_quantity)
        cursor.execute(query)
        con.commit()
        print("data save successfully")


class admin_access():#bakery_offline_order
    #def __init__():
        #bakery_offline_order.__init__(self)

    def log_in_page(self):
        global val5
        print("Enter user name:");enter_user_nm=input()
        print("Enter password:");enter_pass=input()
        cursor.execute('select pass from pass_tab where no=2');va=cursor.fetchall()
        cursor.execute('select pass from pass_tab where no=1');val4=cursor.fetchall()
        for i in va:
            vaa=''.join(i)
        for j in val4:
            vall=''.join(j)
        if enter_user_nm == vaa:
            if vall == enter_pass:
                val5 = 1
        else:
            val5 = 0
            print("Access denied: Wrong login credencials")

    def change_pass_word(self):
        if val5==1:
            id_val=1;new_pas_word=input("Enter new password");comfirm_new_pass=input("Confirm new password")
            if new_pas_word == comfirm_new_pass:
                cursor.execute('delete from pass_tab where no=1');con.commit()
                cursor.execute("insert into pass_tab value({},'{}')".format(id_val,new_pas_word));con.commit()
            else:
                print("confirm password entry does not matches ")
        else:
            val5==0
            print("Access denied")

    def inventory_management(self):
        print("adding new items=1","update stock=2","delete item=3","stock level=4")
        match input('1'or'2'or'3'or'4'):
            case'1':
                 while True:
                     print("Enter product id:");prid=int(input());print("Enter name of product:");nmpr=input();print("quantity:");prquan=int(input())
                     cursor.execute("insert into res_stock value({},'{}',{})".format(prid,nmpr,prquan));con.commit()
                     stp_vr=int(input("enter 1 to adding more & 2 to stop"))
                     if stp_vr==2:
                         break
                 print("added successfully")

            case'2':
                 while True:
                     print("Enter product id, which you want to update:");pr_id=int(input())
                     print(" Type 'A' for adding to stock & Type 'S' for deducting from stock")
                     match input('A'or'S'):
                         case'A':
                             print("Enter quanity you want to add to stock:");add_stk=int(input())
                             cursor.execute('select * from res_stock where product_id={}'.format(pr_id))
                             res_val=cursor.fetchall()
                             for name_of_product,stock_present in res_val:
                                  str_pr_nm=name_of_product;int_st_pr=stock_present
                             str_pr_nm=''.join(str_pr_nm);int_st_pr=int(''.join(map(str,int_st_pr)));print( str_pr_nm,int_st_pr)
                             current_stock_lv=int_st_pr+add_stk
                             cursor.execute("update res_stock set product_id={},name_of_product='{}',stock_present={}").format(pr_id,str_pr_nm,current_stock_lv);con.commit()
                         case'S':
                             print("Enter quantity consumed from stock:");sub_stk=int(input())
                             cursor.execute('select stock_present from res_stock where product_id={}'.format(pr_id))
                             res_val=cursor.fetchall()
                             for i in  res_val:
                                 ec=int(''.join(map(str,i)))
                             ec-=sub_stk
                             cursor.execute("update res_stock set product_id={} where stock_present={}").format(pr_id,ec);con.commit()
                     stp_vr=int(input("enter 1 to update more & 2 to stop"))
                     if stp_vr==2:
                         break

            case'3':
                while True:
                    del_vr=int(input("Enter product id, which is to be deleted:"))
                    cursor.execute("delete from res_stock where product_id={}".format(del_vr));con.commit()
                    stp_vr=int(input("enter 1 to delete more & 2 to stop"))
                    if stp_vr==2:
                        break
                print("product deleted successfully")
            case'4':
                cursor.execute("select * from res_stock");fst_fet=cursor.fetchall()
                items=[];stock_level=[]
                for product_id,name_of_product,stock_present in fst_fet:
                    items.append(name_of_product);stock_level.append(stock_present)
                stock_lv=''.join(map(str,stock_level))
                dict_plot={}
                for key in items:
                    for value in stock_lv:
                        dict_plot[key] = value

                #data = {'milk':5,'chicken':2,'coffee':4,'chocolate':5,'pasta':3}
                items  = dict_plot.keys()
                stock_lv = dict_plot.values()

                fig = plt.figure(figsize = (10, 5))

                print(items,stock_lv,dict_plot)
                plt.bar(items,stock_level, color ='green', width = 0.4)

                plt.xlabel("Items present in stock")
                plt.ylabel("No. of units present")
                plt.title("RESTAURENT GROCERY STOCK")
                plt.show()



    def update_menu_service(self):
        while True:
            print("Enter name of Cake or service:");val1=input();print("Enter price of the previously entered cake or service:");val2=int(input())
            print("In which field, you want to perform addition or updation operation: resmenu=1 addon=2 delivery=3 ")
            match input('1'or'2'or'3'):
                case'1':      #resmenu
                    cursor.execute("Insert into resmenu value('{}',{})".format(val1,val2))
                    con.commit()
                case'2':       #addon
                    cursor.execute("Insert into add_on value('{}',{})".format(val1,val2))
                    con.commit()
                case'3':       #delivery
                    cursor.execute("Insert into delivery value('{}',{})".format(val1,val2))
                    con.commit()

            val3=int(input())
            if val3==2:
                break
        print("data saved successfully")

    def search_oper(self):
        print("In which field, you want to perform search operation: resmenu=1 addon=2 delivery=3 ")
        match input('1'or'2'or'3'):
            case'1':       #resmenu
                cursor.execute("select * from resmenu");search_result=cursor.fetchall()
                for i in search_result:print("deatails of restaurent",i)
            case'2':        #addon
                cursor.execute("select * from add_on");search_result=cursor.fetchall()
                for i in search_result:print("deatails of add_on services",i)
            case'3':        #delivery
                cursor.execute("select * from delivery");search_result=cursor.fetchall()
                for i in search_result:print("deatails of home delivery service",i)

    def delete_operation(self):
        delete_q=input("Enter item for deleteting details:")
        print("In which field, you want to perform delete operation: resmenu=1 addon=2 delivery=3 ")
        match input('1'or'2'or'3'):
            case'1':       #resmenu
                cursor.execute("Delete from resmenu where item='{}'".format(delete_q));con.commit()
            case'2':       #addon
                cursor.execute("Delete from add_on where  add_onitems='{}'".format(delete_q));con.commit()
            case'3':       #delivery
                cursor.execute("Delete from delivery where distance='{}'".format(delete_q));con.commit()
        print("Deleted successfully")

    def show_details(self):
        print("Enter 1 to product csv of current orders & past orders=2")
        match input('1'or'2'):
            case'1':
                cursor.execute('select * from orderdb');sr_re=cursor.fetchall()
                caketyarr=[];date_ofdispatcharr=[];nm_oncakearr=[];date_oforderarr=[];orderidarr=[];amountarr=[];addressarr=[];addonpickarr=[];qua_addonarr=[]
                for cakety,date_ofdispatch,nm_oncake,date_oforder,orderid,amount,address,addonpick,qua_addon in sr_re:
                    caketyarr.append(cakety);date_ofdispatcharr.append(date_ofdispatch);nm_oncakearr.append(nm_oncake);date_oforderarr.append(date_oforder)
                    orderidarr.append(orderid);amountarr.append(amount);addressarr.append(address);addonpickarr.append(addonpick);qua_addonarr.append(qua_addon)

                dict1={'name of cake':caketyarr,'date of dispatch':date_ofdispatcharr,'name on cake':nm_oncakearr,'date of order':date_oforderarr,'order id':orderidarr,'amount':amountarr,'address':addressarr,'addon pick':addonpickarr,'quantity of addon':qua_addonarr}
                df=pd.DataFrame(dict1)
                df_csv=df.to_csv('D:/current_order.csv')
            case'2':
                cursor.execute('select * from delivered_order');sr_re=cursor.fetchall()
                cake_typarr=[];date_of_disptcharr=[];nm_on_cakearr=[];date_of_ordarr=[];order_idarr=[];amountarr=[];addressarr=[];addon_pickarr=[];qun_addonarr=[]
                for cake_typ,date_of_disptch,nm_on_cake,date_of_ord,order_id,amount,address,addon_pick,qun_addon in sr_re:
                    cake_typarr.append(cake_typ);date_of_disptcharr.append(date_of_disptch);nm_on_cakearr.append(nm_on_cake);date_of_ordarr.append(date_of_ord);order_idarr.append(order_id);amountarr.append(amount);addressarr.append(address);addon_pickarr.append(addon_pick);qun_addonarr.append(qun_addon)
                dict2={'name of cake':cake_typarr,'date of dispatch':date_of_disptcharr,'name on cake':nm_on_cakearr,'date of order':date_of_ordarr,'order id':order_idarr,'amount':amountarr,'address':addressarr,'addon pick':addon_pickarr,'quantity of addon':qun_addonarr}
                df=pd.DataFrame(dict2)
                df_csv=df.to_csv('D:/past_order.csv')

    def data_transfer_module(self):
        id_data_trans=int(input("Enter order id of delivered order:"))
        cursor.execute('insert into delivered_order select * from orderdb where orderid={}'.format( id_data_trans));con.commit()
        cursor.execute('delete from orderdb where orderid={}'.format(id_data_trans));con.commit()


if __name__=="__main__":
    pass_v=bakery_offline_order()
    prime_operation=input(print("for new order:NEW or ADMIN"))
    if prime_operation=="NEW":
       #bakery_offline_order()
        pass_v.cake_choice()
        print("Would you like to add other services \n candles:30,baloons:50,decoration:200 ")
        service_1=input(print("Press YES to add or Press SKIP to continue"))
        if service_1=="YES":
            pass_v.addon_choice()
        else:
            service_1=="SKIP"

        print("would you like to opt for home delivery")
        service_2=input("press YES to add service or SKIP to continue")
        if service_2=="YES":
            print("Thanks for choesing us")
            pass_v.homedelivery_choice()
            pass_v.orderid_generation()
            pass_v.details_of_bill()
        else:
            service_2=="SKIP"
            print("Thanks for choesing us")
            pass_v.orderid_generation()
            pass_v.details_of_bill()

    else:

        prime_operation=="ADMIN"
        pas=admin_access()
        pas.log_in_page()
        if val5==1:
            while True:
                print("Enter desiered operation:")
                print("change login password=1","Update menu & service=2","search=3","delete=4","show details of active and past orders=5","data transfer=6","Inventory management=7")
                match input('1'or'2'or'3'or'4'or'5'or'6'or'7'):
                    case'1':
                        pas.change_pass_word()
                    case'2':
                        pas.update_menu_service()
                    case'3':
                        pas.search_oper()
                    case'4':
                        pas.delete_operation()
                    case'5':
                        pas.show_details()
                    case'6':
                        pas.data_transfer_module()
                    case'7':
                        pas.inventory_management()
                brk_val=int(input("Enter 1 to perform other operations \n Enter 2 to exit portal"))
                if brk_val==2:
                    break
