
for $x in doc("q2.xml")/broadway//title
  return
    <result>
      {$x}
    </result>
