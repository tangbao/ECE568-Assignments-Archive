<products>
{
    for $product in doc("q1a.xml")/products/product
    where $product/store/markup = "25%"
    return
        <product>
            {$product/name} {$product/price}
        </product>
}
</products>
