# Things to note about domain application

When a Configuration Restriction record is set for an attribute, product 
configurator applies a domain filter to the attribute in the configuration
wizard in a rather peculiar way.

For example, following attributes and values are available.

Attribute | Values
---|---
Color | Red, White, Black
Size | Small, Large


## Case 1

Attribute | Value | Restriction
---|---|---
Size | Small | Color in Red
Size | Large | Color in White

You might expect that both sizes Small and Large would be available when color
is Black, which is not the case.

You need to create another restriction record so that the complete set of 
records should be as follows to make the configurator behave as expected.

Attribute | Value | Restriction
---|---|---
Size | Small | Color in Red
Size | Large | Color in White
Size | Small, Large | Color in Black


## Case 2

Attribute | Value | Restriction
---|---|---
Size | Small | Color in Red

You may expect that only size Small should be available when color is Red.
However, the configurator makes both size Small and Large available for Red
color. The configurator also makes size Large available for other colors
(White and Black).

This is because Large size does not appear anywhere in the restriction records,
in which case, the configurator judges that the size is available for all
colors.

Therefore, you need to create another restriction record to make Large size
not available for Red color. For example: 

Attribute | Value | Restriction
---|---|---
Size | Small | Color in Red
Size | Small, Large | Color NOT in Red

This way, Large size will only be available in case color is not Red.
