import tkinter as tk 
from tkinter import ttk 
from tkinter import filedialog ,messagebox 
from tkinter import font as tkfont 
import sys 

class IllionViewer :
    def __init__ (self ,root ):
        self .root =root 
        self .root .title ("-illion Numbers Viewer")
        self .root .geometry ("700x500")


        self .base_illions =[
        "Million","Billion","Trillion","Quadrillion","Quintillion",
        "Sextillion","Septillion","Octillion","Nonillion","Decillion"
        ]


        self .base_abbrev =[
        "M","B","T","Qd","Qn","Sx","Sp","Oc","No","De"
        ]


        self .units_base =["","Un","Duo","Tres","Quattuor","Quin","Ses","Septen","Octo","Noven"]
        self .units_abbrev =["","U","D","T","Qt","Qn","Sx","Sp","Oc","No"]


        self .tens_main =["","Deci","Viginti","Triginti","Quadraginti","Quinquaginti",
        "Sexaginti","Septuaginti","Octoginti","Nonaginti"]
        self .tens_main_abbrev =["","De","Vg","Tg","Qg","Qig","Sg","Spg","Og","Ng"]


        self .tens_not_main =["","Deci","Viginti","Triginta","Quadraginta","Quinquaginta",
        "Sexaginta","Septuaginta","Octoginta","Nonaginta"]
        self .tens_not_main_abbrev =["","De","Vg","Tg","Qg","Qig","Sg","Spg","Og","Ng"]


        self .hundreds =["","Centi","Ducenti","Trecenti","Quadringenti","Quingenti",
        "Sescenti","Septingenti","Octingenti","Nongenti"]
        self .hundreds_abbrev =["","Ce","Dct","Tct","Qct","Qict","Sct","Spct","Oct","Nct"]


        self .thousands =["","Milli","Dumilli","Trimilli","Quadrimilli","Quinmilli",
        "Sexmilli","Septimilli","Octimilli","Nonimilli"]
        self .thousands_abbrev =["","Mi","DMi","TMi","QdMi","QnMi","SxMi","SpMi","OcMi","NoMi"]


        self .millions =[
        "","Micri","Dumicri","Trimicri","Quadrimicri","Quinmicri",
        "Sexmicri","Septimicri","Octimicri","Nonimicri"
        ]
        self .millions_abbrev =[
        "","Mc","DMc","TMc","QdMc","QnMc","SxMc","SpMc","OcMc","NoMc"
        ]

        self .billions =["","Nani","Dunani","Trenani","Quadrinani","Quinnani",
        "Sexnani","Septinani","Octinani","Noninani"]
        self .billions_abbrev =["","Nn","DNn","TNn","QdNn","QnNn","SxNn","SpNn","OcNn","NoNn"]


        self .trillions =[
        "","Pici","Dupici","Tripici","Quadripici","Quinpici",
        "Sexpici","Septipici","Octopici","Nonipici"
        ]
        self .trillions_abbrev =["","Pc","DPc","TPc","QdPc","QnPc","SxPc","SpPc","OcPc","NoPc"]

        self .current_index =0 
        self .auto_scroll =False 
        self .scroll_speed =1000 
        self .after_id =None 


        self .max_order =999_999_999_999_999 



        self .settings_window =None 


        self .settings ={
        'bg_color':'#2c3e50',
        'text_color':'#ecf0f1',
        'control_bg':'#34495e',
        'abbrev_color':'#f39c12',
        'order_color':'#3498db',
        'abbrev_size':20 ,
        'text_size':42 ,
        'text_auto_scale':False ,
        'scientific_auto_scale':False ,
        'abbrev_auto_scale':False ,
        'order_size':16 ,
        'scientific_size':24 ,
        'window_width':700 ,
        'unlimited_speed':False ,
        'scroll_increment':1 
        }

        self .setup_ui ()
        self .update_display ()


        self .root .bind ('<Left>',lambda e :self .navigate (-1 ))
        self .root .bind ('<Right>',lambda e :self .navigate (1 ))


        self .root .bind ('<space>',lambda e :self .toggle_auto_scroll ())
        self .root .bind ('<Escape>',lambda e :self .open_settings ())

    def get_unit_prefix (self ,units_digit ,tens_digit ):
        """Get the correct unit prefix based on context and edge cases"""
        if units_digit ==0 :
            return ""


        unit =self .units_base [units_digit ]


        if tens_digit ==1 :
            if units_digit ==3 :
                unit ="Tre"
            elif units_digit ==6 :
                unit ="Sex"
            elif units_digit ==9 :
                unit ="Novem"

        elif tens_digit ==2 :
            if units_digit ==7 :
                unit ="Septem"
            elif units_digit ==9 :
                unit ="Novem"

        elif tens_digit ==6 or tens_digit ==7 :
            if units_digit ==3 :
                unit ="Tre"
            elif units_digit ==6 :
                unit ="Se"

        elif tens_digit ==8 :
            if units_digit ==6 :
                unit ="Sex"
            elif units_digit ==7 :
                unit ="Septem"
            elif units_digit ==9 :
                unit ="Novem"

        elif tens_digit ==9 :
            if units_digit ==3 :
                unit ="Tre"
            elif units_digit ==6 :
                unit ="Se"
            elif units_digit ==7 :
                unit ="Septe"
            elif units_digit ==9 :
                unit ="Nove"

        return unit 

    def generate_illion_name (self ,order ):
        """Generate -illion name based on order (1-indexed)"""

        if order >=1_000_000_000_000 :
            trillions_digit =order //1_000_000_000_000 
            billions_part =(order %1_000_000_000_000 )//1_000_000_000 
            millions_part =(order %1_000_000_000 )//1_000_000 
            thousands_part =(order %1_000_000 )//1000 
            remainder =order %1000 

            name_parts =[]


            if trillions_digit <=9 :
                trillions_prefix =self .trillions [trillions_digit ].lower ()
            else :
                trillions_prefix =self .generate_trillions_prefix (trillions_digit )

            name_parts .append (trillions_prefix )


            if billions_part >0 :
                if billions_part <=9 :
                    billions_prefix =self .billions [billions_part ].lower ()
                else :
                    billions_prefix =self .generate_billions_prefix (billions_part )
                name_parts .append (billions_prefix )


            if millions_part >0 :
                if millions_part <=9 :
                    millions_prefix =self .millions [millions_part ].lower ()
                else :
                    millions_prefix =self .generate_millions_prefix (millions_part )
                name_parts .append (millions_prefix )


            if thousands_part >0 :
                if thousands_part <=9 :
                    thousands_prefix =self .thousands [thousands_part ].lower ()
                else :
                    thousands_prefix =self .generate_thousands_prefix (thousands_part )
                name_parts .append (thousands_prefix )


            if remainder ==0 :
                name ="-".join (name_parts )if len (name_parts )>1 else "".join (name_parts )
                name +="llion"
            else :
                remainder_name =self .generate_illion_name (remainder )
                if remainder_name .lower ().endswith ('llion'):
                    remainder_name =remainder_name [:-5 ]
                elif remainder_name .lower ().endswith ('illion'):
                    remainder_name =remainder_name [:-6 ]

                remainder_name =remainder_name .lower ()
                name_parts .append (remainder_name )

                if thousands_part >0 or millions_part >0 or billions_part >0 :
                    name ="-".join (name_parts )+"llion"
                else :
                    name ="".join (name_parts )+"llion"

            if name :
                name =name [0 ].upper ()+name [1 :]

            return name 


        if order >=1_000_000_000 :
            billions_digit =order //1_000_000_000 
            millions_part =(order %1_000_000_000 )//1_000_000 
            thousands_part =(order %1_000_000 )//1000 
            remainder =order %1000 

            name_parts =[]


            if billions_digit <=9 :
                billion_prefix =self .billions [billions_digit ].lower ()
            else :
                billion_prefix =self .generate_billions_prefix (billions_digit )

            name_parts .append (billion_prefix )


            if millions_part >0 :
                if millions_part <=9 :
                    millions_prefix =self .millions [millions_part ].lower ()
                else :
                    millions_prefix =self .generate_millions_prefix (millions_part )
                name_parts .append (millions_prefix )


            if thousands_part >0 :
                if thousands_part <=9 :
                    thousands_prefix =self .thousands [thousands_part ].lower ()
                else :
                    thousands_prefix =self .generate_thousands_prefix (thousands_part )
                name_parts .append (thousands_prefix )


            if remainder ==0 :
                name ="-".join (name_parts )if len (name_parts )>1 else "".join (name_parts )
                name +="llion"
            else :
                remainder_name =self .generate_illion_name (remainder )
                if remainder_name .lower ().endswith ('llion'):
                    remainder_name =remainder_name [:-5 ]
                elif remainder_name .lower ().endswith ('illion'):
                    remainder_name =remainder_name [:-6 ]

                remainder_name =remainder_name .lower ()
                name_parts .append (remainder_name )

                if thousands_part >0 or millions_part >0 :
                    name ="-".join (name_parts )+"llion"
                else :
                    name ="".join (name_parts )+"llion"

            if name :
                name =name [0 ].upper ()+name [1 :]

            return name 


        if order >=1000000 :
            millions_digit =order //1000000 
            thousands_part =(order %1000000 )//1000 
            remainder =order %1000 

            name_parts =[]


            if millions_digit <=9 :
                million_prefix =self .millions [millions_digit ].lower ()
            else :
                million_prefix =self .generate_millions_prefix (millions_digit )

            name_parts .append (million_prefix )


            if thousands_part >0 :
                if thousands_part <=9 :
                    thousands_prefix =self .thousands [thousands_part ].lower ()
                else :
                    thousands_prefix =self .generate_thousands_prefix (thousands_part )
                name_parts .append (thousands_prefix )


            if remainder ==0 :

                name ="-".join (name_parts )if len (name_parts )>1 and thousands_part >0 else "".join (name_parts )
                name +="llion"
            else :

                remainder_name =self .generate_illion_name (remainder )

                if remainder_name .lower ().endswith ('llion'):
                    remainder_name =remainder_name [:-5 ]
                elif remainder_name .lower ().endswith ('illion'):
                    remainder_name =remainder_name [:-6 ]

                remainder_name =remainder_name .lower ()
                name_parts .append (remainder_name )


                if thousands_part >0 :
                    name ="-".join (name_parts )+"llion"
                else :
                    name ="".join (name_parts )+"llion"


            if name :
                name =name [0 ].upper ()+name [1 :]

            return name 


        if order >=1000 :
            thousands_part =order //1000 
            remainder =order %1000 


            if thousands_part <=9 :

                thousands_prefix =self .thousands [thousands_part ]
            else :

                thousands_prefix =self .generate_thousands_prefix (thousands_part )


            if remainder ==0 :
                name =thousands_prefix +"llion"
            else :

                base_name =self .generate_illion_name (remainder )

                if base_name .lower ().endswith ('llion'):
                    base_name =base_name [:-5 ]
                elif base_name .lower ().endswith ('illion'):
                    base_name =base_name [:-6 ]

                name =thousands_prefix +base_name .lower ()+"llion"


            if name :
                name =name [0 ].upper ()+name [1 :]

            return name 


        if order <=10 :
            name =self .base_illions [order -1 ]
        else :

            hundreds_digit =order //100 
            tens_digit =(order %100 )//10 
            units_digit =order %10 


            tens_is_main =(hundreds_digit ==0 )


            name =""


            name +=self .get_unit_prefix (units_digit ,tens_digit )


            if tens_is_main :
                name +=self .tens_main [tens_digit ]
            else :
                name +=self .tens_not_main [tens_digit ]


            name +=self .hundreds [hundreds_digit ]


            name +="llion"


        if name :
            name =name [0 ].upper ()+name [1 :].lower ()

        return name 

    def generate_thousands_prefix (self ,thousands_value ):
        """Generate prefix for thousands >= 10 using the prefix system on 'milli'"""

        if thousands_value <=9 :
            return self .thousands [thousands_value ].lower ()

        hundreds_digit =thousands_value //100 
        tens_digit =(thousands_value %100 )//10 
        units_digit =thousands_value %10 


        tens_is_main =(hundreds_digit ==0 )


        prefix =""


        prefix +=self .get_unit_prefix (units_digit ,tens_digit )


        if tens_is_main :
            prefix +=self .tens_main [tens_digit ]
        else :
            prefix +=self .tens_not_main [tens_digit ]


        prefix +=self .hundreds [hundreds_digit ]


        prefix =prefix .lower ()


        prefix +="milli"

        return prefix 

    def generate_billions_prefix (self ,billions_value ):
        """Generate prefix for billions >= 10 using the prefix system on 'nani'"""
        if billions_value <=9 :
            return self .billions [billions_value ].lower ()

        hundreds_digit =billions_value //100 
        tens_digit =(billions_value %100 )//10 
        units_digit =billions_value %10 

        tens_is_main =(hundreds_digit ==0 )

        prefix =""
        prefix +=self .get_unit_prefix (units_digit ,tens_digit )

        if tens_is_main :
            prefix +=self .tens_main [tens_digit ]
        else :
            prefix +=self .tens_not_main [tens_digit ]

        prefix +=self .hundreds [hundreds_digit ]

        prefix =prefix .lower ()
        prefix +="nani"

        return prefix 

    def generate_trillions_prefix (self ,trillions_value ):
        """Generate prefix for trillions >= 10 using the prefix system on 'pici'"""
        if trillions_value <=9 :
            return self .trillions [trillions_value ].lower ()

        hundreds_digit =trillions_value //100 
        tens_digit =(trillions_value %100 )//10 
        units_digit =trillions_value %10 

        tens_is_main =(hundreds_digit ==0 )

        prefix =""
        prefix +=self .get_unit_prefix (units_digit ,tens_digit )

        if tens_is_main :
            prefix +=self .tens_main [tens_digit ]
        else :
            prefix +=self .tens_not_main [tens_digit ]

        prefix +=self .hundreds [hundreds_digit ]

        prefix =prefix .lower ()
        prefix +="pici"

        return prefix 

    def generate_billions_abbrev (self ,billions_value ):
        """Generate abbreviation for billions >= 10"""
        if billions_value <=9 :
            return self .billions_abbrev [billions_value ]

        hundreds_digit =billions_value //100 
        tens_digit =(billions_value %100 )//10 
        units_digit =billions_value %10 

        tens_is_main =(hundreds_digit ==0 )

        abbrev =""
        abbrev +=self .units_abbrev [units_digit ]

        if tens_is_main :
            abbrev +=self .tens_main_abbrev [tens_digit ]
        else :
            abbrev +=self .tens_not_main_abbrev [tens_digit ]

        abbrev +=self .hundreds_abbrev [hundreds_digit ]
        abbrev +="Nn"

        return abbrev 

    def generate_trillions_abbrev (self ,trillions_value ):
        """Generate abbreviation for trillions >= 10"""
        if trillions_value <=9 :
            return self .trillions_abbrev [trillions_value ]

        hundreds_digit =trillions_value //100 
        tens_digit =(trillions_value %100 )//10 
        units_digit =trillions_value %10 

        tens_is_main =(hundreds_digit ==0 )

        abbrev =""
        abbrev +=self .units_abbrev [units_digit ]

        if tens_is_main :
            abbrev +=self .tens_main_abbrev [tens_digit ]
        else :
            abbrev +=self .tens_not_main_abbrev [tens_digit ]

        abbrev +=self .hundreds_abbrev [hundreds_digit ]
        abbrev +="Pc"

        return abbrev 

    def generate_millions_prefix (self ,millions_value ):
        """Generate prefix for millions >= 10 using the prefix system on 'micri'"""
        if millions_value <=9 :
            return self .millions [millions_value ].lower ()

        hundreds_digit =millions_value //100 
        tens_digit =(millions_value %100 )//10 
        units_digit =millions_value %10 


        tens_is_main =(hundreds_digit ==0 )


        prefix =""
        prefix +=self .get_unit_prefix (units_digit ,tens_digit )

        if tens_is_main :
            prefix +=self .tens_main [tens_digit ]
        else :
            prefix +=self .tens_not_main [tens_digit ]

        prefix +=self .hundreds [hundreds_digit ]


        prefix =prefix .lower ()


        prefix +="micri"

        return prefix 

    def generate_millions_abbrev (self ,millions_value ):
        """Generate abbreviation for millions >= 10"""
        if millions_value <=9 :
            return self .millions_abbrev [millions_value ]

        hundreds_digit =millions_value //100 
        tens_digit =(millions_value %100 )//10 
        units_digit =millions_value %10 

        tens_is_main =(hundreds_digit ==0 )

        abbrev =""
        abbrev +=self .units_abbrev [units_digit ]

        if tens_is_main :
            abbrev +=self .tens_main_abbrev [tens_digit ]
        else :
            abbrev +=self .tens_not_main_abbrev [tens_digit ]

        abbrev +=self .hundreds_abbrev [hundreds_digit ]
        abbrev +="Mc"

        return abbrev 

    def generate_abbreviation (self ,order ):
        """Generate abbreviation for the given order"""

        if order >=1_000_000_000_000 :
            trillions_digit =order //1_000_000_000_000 
            billions_part =(order %1_000_000_000_000 )//1_000_000_000 
            millions_part =(order %1_000_000_000 )//1_000_000 
            thousands_part =(order %1_000_000 )//1000 
            remainder =order %1000 

            if trillions_digit <=9 :
                abbrev =self .trillions_abbrev [trillions_digit ]
            else :
                abbrev =self .generate_trillions_abbrev (trillions_digit )

            if billions_part >0 :
                if billions_part <=9 :
                    abbrev +=self .billions_abbrev [billions_part ]
                else :
                    abbrev +=self .generate_billions_abbrev (billions_part )

            if millions_part >0 :
                if millions_part <=9 :
                    abbrev +=self .millions_abbrev [millions_part ]
                else :
                    abbrev +=self .generate_millions_abbrev (millions_part )

            if thousands_part >0 :
                if thousands_part <=9 :
                    abbrev +=self .thousands_abbrev [thousands_part ]
                else :
                    abbrev +=self .generate_thousands_abbrev (thousands_part )

            if remainder >0 :
                abbrev +=self .generate_abbreviation (remainder )

            return abbrev 


        if order >=1_000_000_000 :
            billions_digit =order //1_000_000_000 
            millions_part =(order %1_000_000_000 )//1_000_000 
            thousands_part =(order %1_000_000 )//1000 
            remainder =order %1000 

            if billions_digit <=9 :
                abbrev =self .billions_abbrev [billions_digit ]
            else :
                abbrev =self .generate_billions_abbrev (billions_digit )

            if millions_part >0 :
                if millions_part <=9 :
                    abbrev +=self .millions_abbrev [millions_part ]
                else :
                    abbrev +=self .generate_millions_abbrev (millions_part )

            if thousands_part >0 :
                if thousands_part <=9 :
                    abbrev +=self .thousands_abbrev [thousands_part ]
                else :
                    abbrev +=self .generate_thousands_abbrev (thousands_part )

            if remainder >0 :
                abbrev +=self .generate_abbreviation (remainder )

            return abbrev 


        if order >=1000000 :
            millions_digit =order //1000000 
            thousands_part =(order %1000000 )//1000 
            remainder =order %1000 

            if millions_digit <=9 :
                abbrev =self .millions_abbrev [millions_digit ]
            else :
                abbrev =self .generate_millions_abbrev (millions_digit )


            if thousands_part >0 :
                if thousands_part <=9 :
                    abbrev +=self .thousands_abbrev [thousands_part ]
                else :
                    abbrev +=self .generate_thousands_abbrev (thousands_part )


            if remainder >0 :
                abbrev +=self .generate_abbreviation (remainder )

            return abbrev 


        if order >=1000 :
            thousands_part =order //1000 
            remainder =order %1000 


            if thousands_part <=9 :
                thousands_abbrev =self .thousands_abbrev [thousands_part ]
            else :
                thousands_abbrev =self .generate_thousands_abbrev (thousands_part )


            if remainder ==0 :
                return thousands_abbrev 
            else :

                base_abbrev =self .generate_abbreviation (remainder )
                return thousands_abbrev +base_abbrev 


        if order <=10 :
            return self .base_abbrev [order -1 ]
        else :

            hundreds_digit =order //100 
            tens_digit =(order %100 )//10 
            units_digit =order %10 

            tens_is_main =(hundreds_digit ==0 )

            abbrev =""
            abbrev +=self .units_abbrev [units_digit ]

            if tens_is_main :
                abbrev +=self .tens_main_abbrev [tens_digit ]
            else :
                abbrev +=self .tens_not_main_abbrev [tens_digit ]

            abbrev +=self .hundreds_abbrev [hundreds_digit ]

            return abbrev 

    def generate_thousands_abbrev (self ,thousands_value ):
        """Generate abbreviation for thousands >= 10"""
        if thousands_value <=9 :
            return self .thousands_abbrev [thousands_value ]

        hundreds_digit =thousands_value //100 
        tens_digit =(thousands_value %100 )//10 
        units_digit =thousands_value %10 

        tens_is_main =(hundreds_digit ==0 )

        abbrev =""
        abbrev +=self .units_abbrev [units_digit ]

        if tens_is_main :
            abbrev +=self .tens_main_abbrev [tens_digit ]
        else :
            abbrev +=self .tens_not_main_abbrev [tens_digit ]

        abbrev +=self .hundreds_abbrev [hundreds_digit ]
        abbrev +="Mi"

        return abbrev 

    def get_scientific_notation (self ,order ):
        """Calculate scientific notation value: 10^(3 * (order + 1))
        When exponent is too large, express it recursively in scientific notation"""
        exponent =3 *(order +1 )


        threshold =1_000_000 

        if exponent <threshold :
            return f"10^{exponent :,}"
        else :

            exp_str =self .format_exponent (exponent )
            return f"10^({exp_str })"

    def format_exponent (self ,num ):
        """Recursively format large numbers in scientific notation with precise offsets"""

        threshold =1_000_000 

        offset_threshold =100_000 

        if num <threshold :
            return f"{num :,}"


        import math 
        magnitude =int (math .log10 (num ))
        base_power =10 **magnitude 


        coefficient =num //base_power 
        remainder =num -(coefficient *base_power )


        if magnitude <threshold :
            base_str =f"{coefficient }×10^{magnitude :,}"
        else :

            mag_str =self .format_exponent (magnitude )
            base_str =f"{coefficient }×10^({mag_str })"


        if remainder ==0 :
            return base_str 
        elif remainder <offset_threshold :

            return f"{base_str } + {remainder :,}"
        else :

            remainder_str =self .format_exponent (remainder )
            return f"{base_str } + {remainder_str }"

    def get_full_notation (self ,order ):
        """Get the full numeric notation (1 followed by zeros)"""
        exponent =3 *(order +1 )
        return "1"+"0"*exponent 

    def setup_ui (self ):

        self .root .geometry (f"{self .settings ['window_width']}x500")


        display_frame =tk .Frame (self .root ,bg =self .settings ['bg_color'])
        display_frame .pack (fill =tk .BOTH ,expand =True ,padx =20 ,pady =20 )


        settings_btn =tk .Button (
        self .root ,
        text ="⚙",
        command =self .open_settings ,
        font =('Arial',16 ),
        bg ='#7f8c8d',
        fg ='white',
        padx =10 ,
        pady =5 ,
        borderwidth =0 ,
        cursor ='hand2'
        )
        settings_btn .place (x =10 ,y =10 )


        self .order_label =tk .Label (
        display_frame ,
        text ="",
        font =('Arial',self .settings ['order_size'],'bold'),
        bg =self .settings ['bg_color'],
        fg =self .settings .get ('order_color','#3498db')
        )
        self .order_label .pack (pady =(10 ,5 ))


        self .number_label =tk .Label (
        display_frame ,
        text ="",
        font =('Arial',self .settings ['text_size'],'bold'),
        bg =self .settings ['bg_color'],
        fg =self .settings ['text_color'],
        wraplength =self .settings ['window_width']-100 
        )
        self .number_label .pack (pady =10 )


        self .scientific_label =tk .Label (
        display_frame ,
        text ="",
        font =('Arial',self .settings ['scientific_size']),
        bg =self .settings ['bg_color'],
        fg ='#e74c3c'
        )
        self .scientific_label .pack (pady =5 )


        self .abbrev_label =tk .Label (
        display_frame ,
        text ="",
        font =('Arial',self .settings .get ('abbrev_size',20 ),'bold'),
        bg =self .settings ['bg_color'],
        fg =self .settings ['abbrev_color']
        )
        self .abbrev_label .pack (pady =5 )


        self .index_label =tk .Label (
        display_frame ,
        text ="",
        font =('Arial',14 ),
        bg =self .settings ['bg_color'],
        fg ='#95a5a6'
        )
        self .index_label .pack (pady =(5 ,10 ))


        control_frame =tk .Frame (self .root ,bg =self .settings ['control_bg'])
        control_frame .pack (fill =tk .X ,padx =20 ,pady =(0 ,20 ))


        nav_frame =tk .Frame (control_frame ,bg =self .settings ['control_bg'])
        nav_frame .pack (pady =10 )

        tk .Button (
        nav_frame ,
        text ="◄ Previous",
        command =lambda :self .navigate (-1 ),
        font =('Arial',12 ),
        bg ='#3498db',
        fg ='white',
        padx =15 ,
        pady =5 
        ).pack (side =tk .LEFT ,padx =5 )

        tk .Button (
        nav_frame ,
        text ="Next ►",
        command =lambda :self .navigate (1 ),
        font =('Arial',12 ),
        bg ='#3498db',
        fg ='white',
        padx =15 ,
        pady =5 
        ).pack (side =tk .LEFT ,padx =5 )


        jump_frame =tk .Frame (control_frame ,bg =self .settings ['control_bg'])
        jump_frame .pack (pady =5 )

        tk .Label (
        jump_frame ,
        text ="Jump to order:",
        font =('Arial',10 ),
        bg =self .settings ['control_bg'],
        fg ='white'
        ).pack (side =tk .LEFT ,padx =5 )

        self .order_entry =tk .Entry (
        jump_frame ,
        font =('Arial',10 ),
        width =12 
        )
        self .order_entry .pack (side =tk .LEFT ,padx =5 )
        self .order_entry .bind ('<Return>',self .jump_to_order )

        tk .Button (
        jump_frame ,
        text ="Go",
        command =lambda :self .jump_to_order (None ),
        font =('Arial',10 ),
        bg ='#9b59b6',
        fg ='white',
        padx =10 ,
        pady =3 
        ).pack (side =tk .LEFT ,padx =5 )


        auto_frame =tk .Frame (control_frame ,bg =self .settings ['control_bg'])
        auto_frame .pack (pady =5 )

        self .auto_button =tk .Button (
        auto_frame ,
        text ="Start Auto-Scroll",
        command =self .toggle_auto_scroll ,
        font =('Arial',11 ),
        bg ='#2ecc71',
        fg ='white',
        padx =15 ,
        pady =5 
        )
        self .auto_button .pack (side =tk .LEFT ,padx =5 )


        speed_frame =tk .Frame (control_frame ,bg =self .settings ['control_bg'])
        speed_frame .pack (pady =5 )

        tk .Label (
        speed_frame ,
        text ="Speed:",
        font =('Arial',10 ),
        bg =self .settings ['control_bg'],
        fg ='white'
        ).pack (side =tk .LEFT ,padx =5 )


        if self .settings ['unlimited_speed']:

            self .speed_entry =tk .Entry (speed_frame ,font =('Arial',10 ),width =8 )
            self .speed_entry .insert (0 ,str (self .scroll_speed ))
            self .speed_entry .bind ('<Return>',self .update_speed_from_entry )
            self .speed_entry .pack (side =tk .LEFT ,padx =5 )

            tk .Label (
            speed_frame ,
            text ="ms",
            font =('Arial',10 ),
            bg =self .settings ['control_bg'],
            fg ='white'
            ).pack (side =tk .LEFT ,padx =2 )
        else :

            self .speed_scale =ttk .Scale (
            speed_frame ,
            from_ =200 ,
            to =3000 ,
            orient =tk .HORIZONTAL ,
            length =200 ,
            command =self .update_speed 
            )
            self .speed_scale .set (self .scroll_speed )
            self .speed_scale .pack (side =tk .LEFT ,padx =5 )

            self .speed_label =tk .Label (
            speed_frame ,
            text =f"{self .scroll_speed }ms",
            font =('Arial',10 ),
            bg =self .settings ['control_bg'],
            fg ='white',
            width =8 
            )
            self .speed_label .pack (side =tk .LEFT ,padx =5 )

    def update_display (self ):
        order =self .current_index +1 


        illion_name =self .generate_illion_name (order )

        try :
            auto_scale =getattr (self ,'text_autoscale_var',None )
            if auto_scale is None :
                auto_enabled =self .settings .get ('text_auto_scale',False )
            else :
                auto_enabled =bool (auto_scale .get ())
        except Exception :
            auto_enabled =self .settings .get ('text_auto_scale',False )

        base_size =int (self .settings .get ('text_size',42 ))

        if auto_enabled :

            wrap_len =int (self .number_label .cget ('wraplength')or (self .settings .get ('window_width',700 )-100 ))
            font_tmp =tkfont .Font (family ='Arial',size =base_size ,weight ='bold')
            text_width =font_tmp .measure (illion_name )
            if text_width >wrap_len and text_width >0 :
                scale =wrap_len /text_width 
                new_size =max (10 ,int (base_size *scale ))
            else :
                new_size =base_size 

            self .number_label .config (text =illion_name ,font =('Arial',new_size ,'bold'))
        else :

            self .number_label .config (text =illion_name ,font =('Arial',base_size ,'bold'))


        self .order_label .config (text =f"Order: {order }")


        scientific =self .get_scientific_notation (order )

        try :
            sci_var =getattr (self ,'scientific_autoscale_var',None )
            if sci_var is None :
                sci_enabled =self .settings .get ('scientific_auto_scale',False )
            else :
                sci_enabled =bool (sci_var .get ())
        except Exception :
            sci_enabled =self .settings .get ('scientific_auto_scale',False )

        sci_base =int (self .settings .get ('scientific_size',24 ))
        if sci_enabled :
            wrap_len =int (self .scientific_label .cget ('wraplength')or (self .settings .get ('window_width',700 )-100 ))
            font_tmp =tkfont .Font (family ='Arial',size =sci_base )
            sci_width =font_tmp .measure (scientific )
            if sci_width >wrap_len and sci_width >0 :
                scale =wrap_len /sci_width 
                sci_size =max (8 ,int (sci_base *scale ))
            else :
                sci_size =sci_base 
            self .scientific_label .config (text =scientific ,font =('Arial',sci_size ))
        else :
            self .scientific_label .config (text =scientific ,font =('Arial',sci_base ))


        abbrev =self .generate_abbreviation (order )

        try :
            abb_var =getattr (self ,'abbrev_autoscale_var',None )
            if abb_var is None :
                abb_enabled =self .settings .get ('abbrev_auto_scale',False )
            else :
                abb_enabled =bool (abb_var .get ())
        except Exception :
            abb_enabled =self .settings .get ('abbrev_auto_scale',False )

        abb_base =int (self .settings .get ('abbrev_size',20 ))
        if abb_enabled :
            wrap_len =int (self .abbrev_label .cget ('wraplength')or (self .settings .get ('window_width',700 )-100 ))
            font_tmp =tkfont .Font (family ='Arial',size =abb_base ,weight ='bold')
            abb_width =font_tmp .measure (f"Abbrev: {abbrev }")
            if abb_width >wrap_len and abb_width >0 :
                scale =wrap_len /abb_width 
                abb_size =max (8 ,int (abb_base *scale ))
            else :
                abb_size =abb_base 
            self .abbrev_label .config (text =f"Abbrev: {abbrev }",font =('Arial',abb_size ,'bold'))
        else :
            self .abbrev_label .config (text =f"Abbrev: {abbrev }",font =('Arial',abb_base ,'bold'))


        self .index_label .config (text =f"{self .current_index +1 :,} / {self .max_order :,}")

    def navigate (self ,direction ):

        self .current_index =(self .current_index +direction )%self .max_order 
        self .update_display ()

    def jump_to_order (self ,event ):
        """Jump to a specific order number"""
        try :
            order =int (self .order_entry .get ())
            if 1 <=order <=self .max_order :
                self .current_index =order -1 
                self .update_display ()
                self .order_entry .delete (0 ,tk .END )
            else :

                self .order_entry .config (bg ='#e74c3c')
                self .root .after (200 ,lambda :self .order_entry .config (bg ='white'))
        except ValueError :

            self .order_entry .config (bg ='#e74c3c')
            self .root .after (200 ,lambda :self .order_entry .config (bg ='white'))

    def toggle_auto_scroll (self ):
        self .auto_scroll =not self .auto_scroll 

        if self .auto_scroll :
            self .auto_button .config (text ="Stop Auto-Scroll",bg ='#e74c3c')
            self .auto_scroll_step ()
        else :
            self .auto_button .config (text ="Start Auto-Scroll",bg ='#2ecc71')
            if self .after_id :
                self .root .after_cancel (self .after_id )
                self .after_id =None 

    def auto_scroll_step (self ):
        if self .auto_scroll :
            self .navigate (self .settings ['scroll_increment'])
            self .after_id =self .root .after (self .scroll_speed ,self .auto_scroll_step )

    def update_speed (self ,value ):
        self .scroll_speed =int (float (value ))

        if hasattr (self ,'speed_label'):
            self .speed_label .config (text =f"{self .scroll_speed }ms")

    def update_speed_from_entry (self ,event ):
        """Update speed from entry field (for unlimited speed mode)"""
        try :
            speed =int (self .speed_entry .get ())
            if speed >0 :
                self .scroll_speed =speed 
            else :

                self .speed_entry .config (bg ='#e74c3c')
                self .root .after (200 ,lambda :self .speed_entry .config (bg ='white'))
        except ValueError :

            self .speed_entry .config (bg ='#e74c3c')
            self .root .after (200 ,lambda :self .speed_entry .config (bg ='white'))

    def open_settings (self ):
        """Open the settings window"""

        if self .settings_window is not None and self .settings_window .winfo_exists ():
            self .settings_window .lift ()
            return 

        self .settings_window =tk .Toplevel (self .root )
        self .settings_window .title ("Settings")
        self .settings_window .geometry ("600x700")
        self .settings_window .configure (bg ='#2c3e50')


        def on_close ():
            self .settings_window .destroy ()
            self .settings_window =None 

        self .settings_window .protocol ("WM_DELETE_WINDOW",on_close )


        self .settings_window .grab_set ()


        notebook =ttk .Notebook (self .settings_window )
        notebook .pack (fill =tk .BOTH ,expand =True ,padx =10 ,pady =(10 ,60 ))


        general_canvas =tk .Canvas (notebook ,bg ='#34495e',highlightthickness =0 )
        general_frame =tk .Frame (general_canvas ,bg ='#34495e')
        gen_scroll =ttk .Scrollbar (self .settings_window ,orient ='vertical',command =general_canvas .yview )
        general_canvas .create_window ((0 ,0 ),window =general_frame ,anchor ='nw')
        general_canvas .configure (yscrollcommand =gen_scroll .set )
        notebook .add (general_canvas ,text ="General")


        self .create_general_settings (general_frame )


        advanced_frame =tk .Frame (notebook ,bg ='#34495e')
        notebook .add (advanced_frame ,text ="Advanced")
        self .create_advanced_settings (advanced_frame )


        export_frame =tk .Frame (notebook ,bg ='#34495e')
        notebook .add (export_frame ,text ="Export")
        self .create_export_settings (export_frame )


        def _configure_gen (e ):
            general_canvas .configure (scrollregion =general_canvas .bbox ('all'))

        general_frame .bind ('<Configure>',_configure_gen )

        def _bind_gen (ev ):
            self .settings_window .bind_all ('<MouseWheel>',lambda ev2 :general_canvas .yview_scroll (int (-1 *(ev2 .delta /120 )),'units'))
        def _unbind_gen (ev ):
            self .settings_window .unbind_all ('<MouseWheel>')

        general_canvas .bind ('<Enter>',_bind_gen )
        general_canvas .bind ('<Leave>',_unbind_gen )



        sticky_frame =tk .Frame (self .settings_window ,bg ='#2c3e50')
        sticky_frame .place (relx =0 ,rely =1.0 ,relwidth =1.0 ,anchor ='sw')

        button_frame =tk .Frame (sticky_frame ,bg ='#2c3e50')
        button_frame .pack (pady =10 )

        tk .Button (
        button_frame ,
        text ="Apply Changes",
        command =lambda :self .apply_settings (self .settings_window ),
        font =('Arial',12 ),
        bg ='#27ae60',
        fg ='white',
        padx =20 ,
        pady =8 
        ).pack (side =tk .LEFT ,padx =5 )

        tk .Button (
        button_frame ,
        text ="Close",
        command =on_close ,
        font =('Arial',12 ),
        bg ='#e74c3c',
        fg ='white',
        padx =20 ,
        pady =8 
        ).pack (side =tk .LEFT ,padx =5 )

    def create_general_settings (self ,parent ):
        """Create general settings controls"""

        colors_label =tk .Label (parent ,text ="Colors",font =('Arial',14 ,'bold'),bg ='#34495e',fg ='white')
        colors_label .pack (pady =(10 ,5 ),anchor ='w',padx =20 )

        self .create_color_setting (parent ,"Background Color:",'bg_color',0 )

        self .create_color_setting (parent ,"Text Color:",'text_color',1 )

        self .create_color_setting (parent ,"Control Background:",'control_bg',2 )

        self .create_color_setting (parent ,"Abbreviation Color:",'abbrev_color',3 )


        self .create_color_setting (parent ,"Order Color:",'order_color',4 )


        sizes_label =tk .Label (parent ,text ="Sizes",font =('Arial',14 ,'bold'),bg ='#34495e',fg ='white')
        sizes_label .pack (pady =(20 ,5 ),anchor ='w',padx =20 )

        self .create_slider_setting (parent ,"Main Text Size:",'text_size',20 ,80 ,4 )

        self .create_slider_setting (parent ,"Order Text Size:",'order_size',10 ,30 ,5 )

        self .create_slider_setting (parent ,"Scientific Text Size:",'scientific_size',12 ,40 ,6 )

        self .create_slider_setting (parent ,"Window Width:",'window_width',500 ,1200 ,7 )
        self .create_slider_setting (parent ,"Abbreviation Size:",'abbrev_size',8 ,48 ,8 )


        other_label =tk .Label (parent ,text ="Other",font =('Arial',14 ,'bold'),bg ='#34495e',fg ='white')
        other_label .pack (pady =(20 ,5 ),anchor ='w',padx =20 )


        unlimited_frame =tk .Frame (parent ,bg ='#34495e')
        unlimited_frame .pack (fill =tk .X ,padx =20 ,pady =15 )

        self .unlimited_speed_var =tk .BooleanVar (value =self .settings ['unlimited_speed'])

        unlimited_check =tk .Checkbutton (
        unlimited_frame ,
        text ="Disable Scroll Speed Limit (allows any positive integer)",
        variable =self .unlimited_speed_var ,
        font =('Arial',11 ),
        bg ='#34495e',
        fg ='white',
        selectcolor ='#2c3e50',
        activebackground ='#34495e',
        activeforeground ='white'
        )
        unlimited_check .pack (side =tk .LEFT ,padx =5 )


        warning_label =tk .Label (
        unlimited_frame ,
        text ="⚠️",
        font =('Arial',14 ),
        bg ='#34495e',
        fg ='#e67e22',
        cursor ='hand2'
        )
        warning_label .pack (side =tk .LEFT ,padx =5 )


        def show_warning (event ):
            warning_window =tk .Toplevel ()
            warning_window .wm_overrideredirect (True )
            warning_window .wm_geometry (f"+{event .x_root +10 }+{event .y_root +10 }")

            label =tk .Label (
            warning_window ,
            text ="Warning: Very low values (<50ms) may cause\nperformance issues or make the program unresponsive.",
            font =('Arial',9 ),
            bg ='#e67e22',
            fg ='white',
            padx =10 ,
            pady =5 
            )
            label .pack ()

            def hide_warning (e ):
                warning_window .destroy ()

            warning_label .bind ('<Leave>',hide_warning )
            warning_window .bind ('<Leave>',hide_warning )

        warning_label .bind ('<Enter>',show_warning )


        self .create_slider_setting (parent ,"Scroll Increment:",'scroll_increment',1 ,100 ,8 )


        autoscale_frame =tk .Frame (parent ,bg ='#34495e')
        autoscale_frame .pack (fill =tk .X ,padx =20 ,pady =10 )


        self .text_autoscale_var =tk .BooleanVar (value =self .settings .get ('text_auto_scale',False ))

        autoscale_check =tk .Checkbutton (
        autoscale_frame ,
        text ="Text Auto-Scale (shrink long names to fit)",
        variable =self .text_autoscale_var ,
        font =('Arial',11 ),
        bg ='#34495e',
        fg ='white',
        selectcolor ='#2c3e50',
        activebackground ='#34495e',
        activeforeground ='white'
        )
        autoscale_check .pack (side =tk .LEFT ,padx =5 )


        sci_autoscale_frame =tk .Frame (parent ,bg ='#34495e')
        sci_autoscale_frame .pack (fill =tk .X ,padx =20 ,pady =6 )

        self .scientific_autoscale_var =tk .BooleanVar (value =self .settings .get ('scientific_auto_scale',False ))
        sci_check =tk .Checkbutton (
        sci_autoscale_frame ,
        text ="Scientific Notation Auto-Scale",
        variable =self .scientific_autoscale_var ,
        font =('Arial',11 ),
        bg ='#34495e',
        fg ='white',
        selectcolor ='#2c3e50',
        activebackground ='#34495e',
        activeforeground ='white'
        )
        sci_check .pack (side =tk .LEFT ,padx =5 )


        abbrev_autoscale_frame =tk .Frame (parent ,bg ='#34495e')
        abbrev_autoscale_frame .pack (fill =tk .X ,padx =20 ,pady =6 )

        self .abbrev_autoscale_var =tk .BooleanVar (value =self .settings .get ('abbrev_auto_scale',False ))
        abbrev_check =tk .Checkbutton (
        abbrev_autoscale_frame ,
        text ="Abbreviation Auto-Scale",
        variable =self .abbrev_autoscale_var ,
        font =('Arial',11 ),
        bg ='#34495e',
        fg ='white',
        selectcolor ='#2c3e50',
        activebackground ='#34495e',
        activeforeground ='white'
        )
        abbrev_check .pack (side =tk .LEFT ,padx =5 )

    def create_color_setting (self ,parent ,label_text ,setting_key ,row ):
        """Create a color picker setting"""
        frame =tk .Frame (parent ,bg ='#34495e')
        frame .pack (fill =tk .X ,padx =20 ,pady =10 )

        tk .Label (
        frame ,
        text =label_text ,
        font =('Arial',11 ),
        bg ='#34495e',
        fg ='white',
        width =20 ,
        anchor ='w'
        ).pack (side =tk .LEFT ,padx =5 )

        color_entry =tk .Entry (frame ,font =('Arial',11 ),width =15 )
        color_entry .insert (0 ,self .settings [setting_key ])
        color_entry .pack (side =tk .LEFT ,padx =5 )


        if not hasattr (self ,'setting_widgets'):
            self .setting_widgets ={}
        self .setting_widgets [setting_key ]=color_entry 

        def pick_color ():
            from tkinter import colorchooser 

            self .settings_window .grab_release ()
            color =colorchooser .askcolor (initialcolor =self .settings [setting_key ],parent =self .settings_window )

            if self .settings_window .winfo_exists ():
                self .settings_window .grab_set ()
            if color [1 ]:
                color_entry .delete (0 ,tk .END )
                color_entry .insert (0 ,color [1 ])

        tk .Button (
        frame ,
        text ="Pick",
        command =pick_color ,
        font =('Arial',10 ),
        bg ='#3498db',
        fg ='white',
        padx =10 
        ).pack (side =tk .LEFT ,padx =5 )

    def create_slider_setting (self ,parent ,label_text ,setting_key ,min_val ,max_val ,row ):
        """Create a slider setting"""
        frame =tk .Frame (parent ,bg ='#34495e')
        frame .pack (fill =tk .X ,padx =20 ,pady =10 )

        tk .Label (
        frame ,
        text =label_text ,
        font =('Arial',11 ),
        bg ='#34495e',
        fg ='white',
        width =20 ,
        anchor ='w'
        ).pack (side =tk .LEFT ,padx =5 )

        value_label =tk .Label (
        frame ,
        text =str (self .settings [setting_key ]),
        font =('Arial',11 ),
        bg ='#34495e',
        fg ='white',
        width =6 
        )
        value_label .pack (side =tk .RIGHT ,padx =5 )

        slider =ttk .Scale (
        frame ,
        from_ =min_val ,
        to =max_val ,
        orient =tk .HORIZONTAL ,
        length =200 ,
        command =lambda v :value_label .config (text =str (int (float (v ))))
        )
        slider .set (self .settings [setting_key ])
        slider .pack (side =tk .RIGHT ,padx =5 )

        if not hasattr (self ,'setting_widgets'):
            self .setting_widgets ={}
        self .setting_widgets [setting_key ]=slider 

    def create_advanced_settings (self ,parent ):
        """Create advanced settings for prefix editing"""

        canvas =tk .Canvas (parent ,bg ='#34495e',highlightthickness =0 )
        scrollbar =ttk .Scrollbar (parent ,orient ="vertical",command =canvas .yview )
        scrollable_frame =tk .Frame (canvas ,bg ='#34495e')

        scrollable_frame .bind (
        "<Configure>",
        lambda e :canvas .configure (scrollregion =canvas .bbox ("all"))
        )

        canvas .create_window ((0 ,0 ),window =scrollable_frame ,anchor ="nw")
        canvas .configure (yscrollcommand =scrollbar .set )

        canvas .pack (side ="left",fill ="both",expand =True )
        scrollbar .pack (side ="right",fill ="y")


        def _on_mousewheel (event ):

            try :
                if sys .platform =='darwin':

                    step =int (-1 *event .delta )
                else :

                    raw =int (event .delta )
                    step =int (raw /120 )if raw !=0 else 0 
                    if step ==0 :

                        step =1 if raw >0 else -1 

                canvas .yview_scroll (-step ,"units")
            except Exception :
                return 

        def _bind_to_mousewheel (event ):


            target =self .settings_window if getattr (self ,'settings_window',None )else canvas 
            target .bind_all ("<MouseWheel>",_on_mousewheel )

            target .bind_all ("<Button-4>",lambda e :canvas .yview_scroll (-1 ,"units"))
            target .bind_all ("<Button-5>",lambda e :canvas .yview_scroll (1 ,"units"))

        def _unbind_from_mousewheel (event ):
            target =self .settings_window if getattr (self ,'settings_window',None )else canvas 
            target .unbind_all ("<MouseWheel>")
            target .unbind_all ("<Button-4>")
            target .unbind_all ("<Button-5>")



        canvas .bind ('<Enter>',_bind_to_mousewheel )
        canvas .bind ('<Leave>',_unbind_from_mousewheel )
        scrollbar .bind ('<Enter>',_bind_to_mousewheel )
        scrollbar .bind ('<Leave>',_unbind_from_mousewheel )


        tk .Label (
        scrollable_frame ,
        text ="Units Prefixes & Abbreviations (0-9):",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(10 ,5 ))

        self .units_entries =[]
        self .units_abbrev_entries =[]
        for i ,(unit ,abbrev )in enumerate (zip (self .units_base ,self .units_abbrev )):
            self .create_prefix_abbrev_entry (scrollable_frame ,f"{i }:",unit ,abbrev ,
            self .units_entries ,self .units_abbrev_entries )


        tk .Label (
        scrollable_frame ,
        text ="Tens Prefixes - Main (with -i ending) & Abbreviations:",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(15 ,5 ))

        self .tens_main_entries =[]
        self .tens_main_abbrev_entries =[]
        tens_names =["0","Deci","Viginti","Triginti","Quadraginti","Quinquaginti",
        "Sexaginti","Septuaginti","Octoginti","Nonaginti"]
        for i ,(tens ,abbrev )in enumerate (zip (self .tens_main ,self .tens_main_abbrev )):
            self .create_prefix_abbrev_entry (scrollable_frame ,tens_names [i ]+":",tens ,abbrev ,
            self .tens_main_entries ,self .tens_main_abbrev_entries )


        tk .Label (
        scrollable_frame ,
        text ="Tens Prefixes - Not Main (with -a ending) & Abbreviations:",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(15 ,5 ))

        self .tens_not_main_entries =[]
        self .tens_not_main_abbrev_entries =[]
        for i ,(tens ,abbrev )in enumerate (zip (self .tens_not_main ,self .tens_not_main_abbrev )):
            self .create_prefix_abbrev_entry (scrollable_frame ,tens_names [i ]+":",tens ,abbrev ,
            self .tens_not_main_entries ,self .tens_not_main_abbrev_entries )


        tk .Label (
        scrollable_frame ,
        text ="Hundreds Prefixes & Abbreviations:",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(15 ,5 ))

        self .hundreds_entries =[]
        self .hundreds_abbrev_entries =[]
        hundreds_names =["0","Centi","Ducenti","Trecenti","Quadringenti","Quingenti",
        "Sescenti","Septingenti","Octingenti","Nongenti"]
        for i ,(hundred ,abbrev )in enumerate (zip (self .hundreds ,self .hundreds_abbrev )):
            self .create_prefix_abbrev_entry (scrollable_frame ,hundreds_names [i ]+":",hundred ,abbrev ,
            self .hundreds_entries ,self .hundreds_abbrev_entries )


        tk .Label (
        scrollable_frame ,
        text ="Thousands Prefixes & Abbreviations (0-9):",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(15 ,5 ))

        self .thousands_entries =[]
        self .thousands_abbrev_entries =[]
        thousands_names =["0","Milli (1000)","Dumilli (2000)","Trimilli (3000)","Quadrimilli (4000)",
        "Quinmilli (5000)","Sexmilli (6000)","Septimilli (7000)","Octimilli (8000)","Nonimilli (9000)"]
        for i ,(thousand ,abbrev )in enumerate (zip (self .thousands ,self .thousands_abbrev )):
            self .create_prefix_abbrev_entry (scrollable_frame ,thousands_names [i ]+":",thousand ,abbrev ,
            self .thousands_entries ,self .thousands_abbrev_entries )


        tk .Label (
        scrollable_frame ,
        text ="Millions Prefix & Abbreviation:",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(15 ,5 ))

        self .millions_entry_list =[]
        self .millions_abbrev_entry_list =[]

        for i ,(mil ,mabbr )in enumerate (zip (self .millions ,self .millions_abbrev )):
            label =f"{i }:"
            self .create_prefix_abbrev_entry (scrollable_frame ,label ,mil ,mabbr ,
            self .millions_entry_list ,self .millions_abbrev_entry_list )


        tk .Label (
        scrollable_frame ,
        text ="Billions Prefix & Abbreviation:",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(15 ,5 ))

        self .billions_entry_list =[]
        self .billions_abbrev_entry_list =[]

        for i ,(bll ,babbr )in enumerate (zip (self .billions ,self .billions_abbrev )):
            label =f"{i }:"
            self .create_prefix_abbrev_entry (scrollable_frame ,label ,bll ,babbr ,
            self .billions_entry_list ,self .billions_abbrev_entry_list )


        tk .Label (
        scrollable_frame ,
        text ="Trillions Prefix & Abbreviation:",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(15 ,5 ))

        self .trillions_entry_list =[]
        self .trillions_abbrev_entry_list =[]
        for i ,(trl ,tabbr )in enumerate (zip (self .trillions ,self .trillions_abbrev )):
            label =f"{i }:"
            self .create_prefix_abbrev_entry (scrollable_frame ,label ,trl ,tabbr ,
            self .trillions_entry_list ,self .trillions_abbrev_entry_list )

    def create_export_settings (self ,parent ):
        """Create Export tab UI for CSV export"""
        frame =tk .Frame (parent ,bg ='#34495e')
        frame .pack (fill =tk .BOTH ,expand =True ,padx =10 ,pady =10 )

        tk .Label (
        frame ,
        text ="Export Range to CSV (semicolon-separated):",
        font =('Arial',12 ,'bold'),
        bg ='#34495e',
        fg ='white'
        ).pack (pady =(5 ,10 ))


        opts_frame =tk .Frame (frame ,bg ='#34495e')
        opts_frame .pack (fill =tk .X ,padx =20 ,pady =5 )

        self .include_order_var =tk .BooleanVar (value =True )
        self .include_fullname_var =tk .BooleanVar (value =True )
        self .include_abbrev_var =tk .BooleanVar (value =True )
        self .include_value_var =tk .BooleanVar (value =True )

        order_cb =tk .Checkbutton (opts_frame ,text ="Include Order",variable =self .include_order_var ,
        font =('Arial',11 ),bg ='#34495e',fg ='white',selectcolor ='#2c3e50',
        activebackground ='#34495e',activeforeground ='white',command =self .update_export_button_state )
        order_cb .pack (anchor ='w')

        fullname_cb =tk .Checkbutton (opts_frame ,text ="Include Full Name",variable =self .include_fullname_var ,
        font =('Arial',11 ),bg ='#34495e',fg ='white',selectcolor ='#2c3e50',
        activebackground ='#34495e',activeforeground ='white',command =self .update_export_button_state )
        fullname_cb .pack (anchor ='w')

        abbrev_cb =tk .Checkbutton (opts_frame ,text ="Include Abbreviation",variable =self .include_abbrev_var ,
        font =('Arial',11 ),bg ='#34495e',fg ='white',selectcolor ='#2c3e50',
        activebackground ='#34495e',activeforeground ='white',command =self .update_export_button_state )
        abbrev_cb .pack (anchor ='w')

        value_cb =tk .Checkbutton (opts_frame ,text ="Include Value (scientific)",variable =self .include_value_var ,
        font =('Arial',11 ),bg ='#34495e',fg ='white',selectcolor ='#2c3e50',
        activebackground ='#34495e',activeforeground ='white',command =self .update_export_button_state )
        value_cb .pack (anchor ='w')


        range_frame =tk .Frame (frame ,bg ='#34495e')
        range_frame .pack (fill =tk .X ,padx =20 ,pady =10 )

        tk .Label (range_frame ,text ="Start Order:",font =('Arial',10 ),bg ='#34495e',fg ='white',width =12 ,anchor ='w').pack (side =tk .LEFT )
        self .export_start_entry =tk .Entry (range_frame ,font =('Arial',10 ),width =12 )
        self .export_start_entry .pack (side =tk .LEFT ,padx =5 )
        self .export_start_entry .insert (0 ,"1")

        tk .Label (range_frame ,text ="End Order:",font =('Arial',10 ),bg ='#34495e',fg ='white',width =10 ,anchor ='w').pack (side =tk .LEFT ,padx =(10 ,0 ))
        self .export_end_entry =tk .Entry (range_frame ,font =('Arial',10 ),width =12 )
        self .export_end_entry .pack (side =tk .LEFT ,padx =5 )
        self .export_end_entry .insert (0 ,"100")


        btn_frame =tk .Frame (frame ,bg ='#34495e')
        btn_frame .pack (pady =15 )

        self .export_button =tk .Button (btn_frame ,text ="Export to CSV",command =self .export_to_csv ,
        font =('Arial',12 ),bg ='#2980b9',fg ='white',padx =20 ,pady =8 )
        self .export_button .pack ()


        self .update_export_button_state ()

    def update_export_button_state (self ):
        """Enable export button only if at least one include option is selected"""
        if any ([self .include_order_var .get (),self .include_fullname_var .get (),self .include_abbrev_var .get (),self .include_value_var .get ()]):
            self .export_button .config (state =tk .NORMAL ,bg ='#2980b9')
        else :
            self .export_button .config (state =tk .DISABLED ,bg ='#7f8c8d')

    def export_to_csv (self ):
        """Validate inputs and export the selected range to CSV (semicolon-separated)"""

        include_order =self .include_order_var .get ()
        include_fullname =self .include_fullname_var .get ()
        include_abbrev =self .include_abbrev_var .get ()
        include_value =self .include_value_var .get ()

        if not any ([include_order ,include_fullname ,include_abbrev ,include_value ]):
            messagebox .showerror ("Export Error","Select at least one field to include in export.")
            return 


        try :
            start =int (self .export_start_entry .get ())
            end =int (self .export_end_entry .get ())
        except ValueError :
            messagebox .showerror ("Export Error","Start and End must be integers.")
            return 

        if start <1 or end <1 or start >self .max_order or end >self .max_order :
            messagebox .showerror ("Export Error",f"Start and End must be between 1 and {self .max_order :,}.")
            return 

        if start >end :
            messagebox .showerror ("Export Error","Start must be less than or equal to End.")
            return 


        save_path =filedialog .asksaveasfilename (defaultextension ='.csv',filetypes =[('CSV files','*.csv'),('All files','*.*')])
        if not save_path :
            return 


        headers =[]
        if include_order :
            headers .append ('order')
        if include_fullname :
            headers .append ('full_name')
        if include_abbrev :
            headers .append ('abbreviation')
        if include_value :
            headers .append ('value')

        try :
            with open (save_path ,'w',encoding ='utf-8',newline ='')as f :
                f .write (';'.join (headers )+'\n')


                for order in range (start ,end +1 ):
                    parts =[]
                    if include_order :
                        parts .append (str (order ))
                    if include_fullname :
                        parts .append (self .generate_illion_name (order ))
                    if include_abbrev :
                        parts .append (self .generate_abbreviation (order ))
                    if include_value :
                        parts .append (self .get_scientific_notation (order ))


                    f .write (';'.join (parts )+'\n')

            messagebox .showinfo ("Export Complete",f"Exported orders {start } to {end } to:\n{save_path }")
        except Exception as e :
            messagebox .showerror ("Export Error",f"Failed to export CSV:\n{e }")

    def create_prefix_entry (self ,parent ,label_text ,current_value ,storage_list ):
        """Create an entry for editing prefixes"""
        frame =tk .Frame (parent ,bg ='#34495e')
        frame .pack (fill =tk .X ,padx =20 ,pady =2 )

        tk .Label (
        frame ,
        text =label_text ,
        font =('Arial',10 ),
        bg ='#34495e',
        fg ='white',
        width =15 ,
        anchor ='w'
        ).pack (side =tk .LEFT ,padx =5 )

        entry =tk .Entry (frame ,font =('Arial',10 ),width =20 )
        entry .insert (0 ,current_value )
        entry .pack (side =tk .LEFT ,padx =5 )

        storage_list .append (entry )

    def create_prefix_abbrev_entry (self ,parent ,label_text ,prefix_value ,abbrev_value ,
    prefix_storage ,abbrev_storage ):
        """Create entries for editing both prefix and abbreviation"""
        frame =tk .Frame (parent ,bg ='#34495e')
        frame .pack (fill =tk .X ,padx =20 ,pady =2 )


        tk .Label (
        frame ,
        text =label_text ,
        font =('Arial',10 ),
        bg ='#34495e',
        fg ='white',
        width =15 ,
        anchor ='w'
        ).pack (side =tk .LEFT ,padx =5 )


        prefix_entry =tk .Entry (frame ,font =('Arial',10 ),width =15 )
        prefix_entry .insert (0 ,prefix_value )
        prefix_entry .pack (side =tk .LEFT ,padx =5 )


        tk .Label (
        frame ,
        text ="→",
        font =('Arial',10 ),
        bg ='#34495e',
        fg ='#95a5a6'
        ).pack (side =tk .LEFT ,padx =2 )


        abbrev_entry =tk .Entry (frame ,font =('Arial',10 ),width =10 )
        abbrev_entry .insert (0 ,abbrev_value )
        abbrev_entry .pack (side =tk .LEFT ,padx =5 )

        prefix_storage .append (prefix_entry )
        abbrev_storage .append (abbrev_entry )

    def apply_settings (self ,window ):
        """Apply all settings changes"""

        for key ,widget in self .setting_widgets .items ():
            if isinstance (widget ,tk .Entry ):
                self .settings [key ]=widget .get ()
            elif isinstance (widget ,ttk .Scale ):
                self .settings [key ]=int (widget .get ())


        if hasattr (self ,'unlimited_speed_var'):
            self .settings ['unlimited_speed']=self .unlimited_speed_var .get ()

        if hasattr (self ,'text_autoscale_var'):
            self .settings ['text_auto_scale']=self .text_autoscale_var .get ()

        if hasattr (self ,'scientific_autoscale_var'):
            self .settings ['scientific_auto_scale']=self .scientific_autoscale_var .get ()
        if hasattr (self ,'abbrev_autoscale_var'):
            self .settings ['abbrev_auto_scale']=self .abbrev_autoscale_var .get ()


        if hasattr (self ,'base_illions_entries'):
            self .base_illions =[entry .get ()for entry in self .base_illions_entries ]
            self .base_abbrev =[entry .get ()for entry in self .base_abbrev_entries ]

        if hasattr (self ,'units_entries'):
            self .units_base =[entry .get ()for entry in self .units_entries ]
            self .units_abbrev =[entry .get ()for entry in self .units_abbrev_entries ]

            self .tens_main =[entry .get ()for entry in self .tens_main_entries ]
            self .tens_main_abbrev =[entry .get ()for entry in self .tens_main_abbrev_entries ]

            self .tens_not_main =[entry .get ()for entry in self .tens_not_main_entries ]
            self .tens_not_main_abbrev =[entry .get ()for entry in self .tens_not_main_abbrev_entries ]

            self .hundreds =[entry .get ()for entry in self .hundreds_entries ]
            self .hundreds_abbrev =[entry .get ()for entry in self .hundreds_abbrev_entries ]

            if hasattr (self ,'thousands_entries')and self .thousands_entries :
                self .thousands =[entry .get ()for entry in self .thousands_entries ]
                self .thousands_abbrev =[entry .get ()for entry in self .thousands_abbrev_entries ]

            if hasattr (self ,'millions_entry_list')and self .millions_entry_list :
                self .millions =[entry .get ()for entry in self .millions_entry_list ]
                self .millions_abbrev =[entry .get ()for entry in self .millions_abbrev_entry_list ]

            if hasattr (self ,'billions_entry_list')and self .billions_entry_list :
                self .billions =[entry .get ()for entry in self .billions_entry_list ]
                self .billions_abbrev =[entry .get ()for entry in self .billions_abbrev_entry_list ]

            if hasattr (self ,'trillions_entry_list')and self .trillions_entry_list :
                self .trillions =[entry .get ()for entry in self .trillions_entry_list ]
                self .trillions_abbrev =[entry .get ()for entry in self .trillions_abbrev_entry_list ]


        for widget in self .root .winfo_children ():
            widget .destroy ()

        self .setup_ui ()
        self .update_display ()


        self .settings_window =None 
        window .destroy ()

if __name__ =="__main__":
    root =tk .Tk ()
    app =IllionViewer (root )
    root .mainloop ()