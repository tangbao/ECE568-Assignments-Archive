for $x in doc("q2.xml")/broadway/concert[type = "chamber orchestra"]
  where avg(data($x/price))>=50
  return
  <result>
    {$x/title}
  </result>