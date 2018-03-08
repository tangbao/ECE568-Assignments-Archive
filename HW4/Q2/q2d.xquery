for $d in distinct-values(doc("q2.xml")//date)
  for $x in //theater[date = $d] | //concert[date = $d] | //opera[date=$d]
    return
      <groupByDate>
            <day>
              {$d}
              <show>
                {$x/title}
                {$x/price}
              </show>
            </day>
      </groupByDate>