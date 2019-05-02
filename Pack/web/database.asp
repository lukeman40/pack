<html>
<head>
  <title></title>
<style type="text/css">
.style {
	color: #003;
	left: 100px;
	margin-left: 0px;
	padding-left: 200px;
}
#Height1 {
	color: #003;
	font-family: Tahoma, Geneva, sans-serif;
}
.Main {
	color: #D6D6D6;
}
body {
	background-color: #fffEFF;
}
</style>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body class="Main">


<h1>Contents</h1>
<ul>

</ul>

<%
set conn=Server.CreateObject("ADODB.Connection")
conn.Provider="Microsoft.Jet.OLEDB.4.0"
conn.Open "C:\Users\Luke\PycharmProjects\Excel\Pack\web\test.mdb"

set rs = Server.CreateObject("ADODB.recordset")
rs.Open "SELECT * FROM Customers", conn

do until rs.EOF
  for each x in rs.Fields
    Response.Write(x.name)
    Response.Write(" = ")
    Response.Write(x.value & "<br>")
  next
  Response.Write("<br>")
  rs.MoveNext
loop

rs.close
conn.close
%>


</body>
</html>