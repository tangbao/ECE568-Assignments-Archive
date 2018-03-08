for $x in doc("q2.xml")/broadway/theater[date = "11/9/2008"]
  where some $b in $x/price satisfies data($b) < 35
  return
    <theater>
      {$x/title}{$x/address}
    </theater>