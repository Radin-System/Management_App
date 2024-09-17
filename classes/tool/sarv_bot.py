from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from ._base import WebBot

class SarvBot(WebBot):
    def Login(self,Username,Password) -> None:
        self.Get("index.php?action=Login&module=Users&login_module=Home&login_action=index&utype=radin1")

        self.Fill_Input(By.ID, "user_name",Username)
        self.Fill_Input(By.ID, "user_password",Password)
        self.Click_Element(By.ID, "LoginButton")

    def Select_Radio(self,MultiSelect_By:By,Identifire:str,Select:str) -> None : 
        MultiSelect = self.Click_Element(MultiSelect_By,Identifire)
        self.Driver.find_element(By.TAG_NAME, "input")

        self.Sleep(0.2)
        Options = [Option for Option in MultiSelect.find_elements(By.TAG_NAME,'label')]
        for Option in Options :
            try : Selection = Option.find_element(By.TAG_NAME,"input")
            except : continue
            if Selection.get_attribute("type") != "radio" : 
                Options.remove(Option)
                continue
            if Option.text == Select :
                self.Sleep(0.2)
                Selection.click()

    def Get_Account_Detail(self,ID) -> dict:
        self.Get(f"{self.Base_URL}index.php?module=Accounts&action=EditView&record={ID}")

        Name = self.Driver.find_element(By.CLASS_NAME,"view_form_buttons_title").text
        Tabel = self.Driver.find_element(By.ID,"AccountsphoneNumbersTable")
        divs = Tabel.find_elements(By.TAG_NAME,"input")
        Numbers = []
        for div in divs :
            if "phoneNumber" in div.get_attribute("id") and "text" == div.get_attribute("type") :
                Numbers.append(div.get_attribute("value"))
        
        return {
            "ID" : ID,
            "Name" : Name,
            "Numbers" : Numbers,
        }

    def Get_Contact_By_CID(self,CID) -> dict:
        self.Get(f"index.php?module=Customer_Console&callerid={CID}")
        Caller_Detail = {}

        Status_Bar = self.Driver.find_elements(By.CLASS_NAME,"colorBox")
        Caller_Detail["Parent_Type"] = Status_Bar[0].text
        Caller_Detail["CID"]         = Status_Bar[1].text if Status_Bar[1].text else CID
        Caller_Detail["Phone_Type"]  = Status_Bar[2].text if Status_Bar[2].text else "سایر"

        InformationPanel = self.Driver.find_element(By.ID,"informationPanel")
        Divs = InformationPanel.find_elements(By.TAG_NAME,"div")

        Name = ""
        for Div in Divs :
            for Section in Div.find_elements(By.TAG_NAME,"div") :
                if "نام و نام خانوادگی" in Section.text : 
                    Name = Section.text.replace("نام و نام خانوادگی",'')
                    break

        Caller_Detail["Name"] = Name

        return Caller_Detail

    def Add_Call(self,Parent_Type:str, From:str, User:str, Extension:str, DebugData:str, CID:str) -> str :
        self.Get("index.php?module=Calls&action=EditView")

        self.Fill_Input(By.ID, "name", "تماس ورودی از "+" "+From if From else "تماس ورودی ناشناس"+" "+CID)

        From = "آقای نا شناس" if not From else From
        Parent_Type = "فرد" if not Parent_Type else Parent_Type

        self.Select_Radio(By.ID,"parent_type_multiselect",Parent_Type)
        self.Fill_Input(By.ID,"parent_name",From)
        self.Select_Radio(By.ID,"status_multiselect","انجام شده")
        self.Select_Radio(By.ID,"direction_multiselect","ورودی")
        self.Fill_Input(By.ID, "assigned_user_name",User)
        self.Fill_Input(By.ID, "voip_id",Extension)
        self.Fill_Input(By.ID, "debugfield",DebugData)

    def Get_List(self,Module:str,Search:str,Column_Header) -> list[WebElement] :
        self.Get(f"index.php?module={Module}&action=index")
        self.Select_Radio(By.ID,"saved_search_select_multiselect",Select=Search)
        
        Form = self.Driver.find_element(By.ID,'MassUpdate')
        Table = Form.find_element(By.TAG_NAME,'table')
        Rows = Table.find_elements(By.TAG_NAME,'tr')
        
        Header_Values = Rows.pop(0).find_elements(By.TAG_NAME,'th')

        Result = []
        for Row in Rows:
            Row_Values = Row.find_elements(By.TAG_NAME, 'td')
            for Header, Value in zip(Header_Values, Row_Values):
                if Header.text == Column_Header : Result.append(Value)
                continue

        return Result

    def Add_or_Edit(self,Module:str,Record:str=None,Submit = False,**Kwargs:dict) :
        Record = f'&record={Record}' if Record is not None else ''
        self.Get(f'index.php?module={Module}&action=EditView')

        for Key , Value in Kwargs.items() :
            if Value['Type'] == 'input' : self.Fill_Input(By.ID,Key,Value['Value'],Click=True,Clear=True)
            if Value['Type'] == 'text'  : self.Fill_Input(By.ID,Key,Value['Value'],Clear=True)
            if Value['Type'] == 'date'  : self.Fill_Input(By.ID,Key,Value['Value'])
            if Value['Type'] == 'multi' : self.Select_Radio(By.ID,Key,Value['Value'])

        Form = self.Driver.find_element(By.ID,'EditView')
        Button_Bar = Form.find_element(By.CLASS_NAME,'view_form_buttons_buttons')
        Buttons = Button_Bar.find_elements(By.TAG_NAME,'input')

        for Input in Buttons :
            if Input.get_attribute('value') == 'ذخیره' : 
                if Submit : Input.click()
                break