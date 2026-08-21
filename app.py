# Color & Keyword Detection Logic (Fixed for Strawberries & Red Fruits)
        img_np = np.array(image.resize((100, 100)))
        r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]

        # Detect Red/Pink (Strawberry, Apple) vs Green (Vegetables) vs White (Dairy)
        is_red_or_fruit = np.mean((r > g) & (r > b)) > 0.20
        is_green = np.mean((g > r) & (g > b)) > 0.35
        is_white_packaging = (
            np.mean((r > 190) & (g > 190) & (b > 190)) > 0.45
        )

        fruit_keywords = [
            'fruit',
            'strawberry',
            'apple',
            'banana',
            'mango',
            'فراولة',
            'تفاح',
            'موز',
            'فواكه',
            'garden',
        ]
        veg_keywords = ['veg', 'tomato', 'cucumber', 'خيار', 'طماطم', 'خضار']
        dairy_keywords = [
            'dairy',
            'milk',
            'yoghurt',
            'yogurt',
            'almarai',
            'laban',
            'cheese',
            'لبن',
            'زبادي',   'جبنة',
        ]

        if any(
            k in file_name for k in fruit_keywords
        ) or (is_red_or_fruit and not is_white_packaging):
          cat_key = 'Fruits'
        elif any(k in file_name for k in veg_keywords) or (
            is_green and not is_white_packaging
        ):
          cat_key = 'Vegetables'
        elif (
            any(k in file_name for k in dairy_keywords)
            or is_white_packaging
        ):
          cat_key = 'Dairy'
        else:
          cat_key = 'Fruits'
