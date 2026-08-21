if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_container_width=True)

    with st.spinner("Analyzing image and container structure..."):
        file_name = uploaded_file.name.lower()
        
        # Color distribution analysis for packaging
        img_np = np.array(image.resize((100, 100)))
        avg_white = np.mean(img_np > 200)
        
        # Keywords
        is_dairy_keyword = any(k in file_name for k in ['yoghurt', 'yogurt', 'milk', 'almarai', 'laban', 'cheese', 'test3'])
        is_fruit_keyword = any(k in file_name for k in ['mango', 'apple', 'banana', 'strawberry', 'fruit', 'تفاح', 'موز', 'مانجو'])
        is_veg_keyword = any(k in file_name for k in ['tomato', 'vegetable', 'cucumber', ' خيار', 'طماطم', 'خضار'])

        # Corrected Classification Priority:
        # 1. Check direct fruit/vegetable keywords first
        if is_dairy_keyword and is_fruit_keyword:
            cat_key = 'Fruit_Dairy'
            detected_label = "زبادي بنكهة الفواكه (Fruit Yoghurt)" if lang == 'ar' else "Fruit Flavored Yoghurt"
        elif is_fruit_keyword:
            cat_key = 'Fruits'
            detected_label = "فواكه طازجة (Fresh Fruits)" if lang == 'ar' else "Fresh Fruits"
        elif is_veg_keyword:
            cat_key = 'Vegetables'
            detected_label = "خضروات طازجة (Fresh Vegetables)" if lang == 'ar' else "Fresh Vegetables"
        elif is_dairy_keyword:
            cat_key = 'Dairy'
            detected_label = "زبادي / منتجات ألبان (Dairy Yoghurt)" if lang == 'ar' else "Dairy / Yoghurt Product"
        elif avg_white > 0.65:  # Raised threshold to prevent false positives from light backgrounds
            cat_key = 'Dairy'
            detected_label = "زبادي / منتجات ألبان (Dairy Yoghurt)" if lang == 'ar' else "Dairy / Yoghurt Product"
        else:
            cat_key = 'Default'
            detected_label = class_names[0] if class_names else ("منتج عام" if lang == 'ar' else "General Product")

        # Result Display
        st.subheader(t['result_header'])
        st.success(f"**{detected_label}**")

        st.markdown("---")

        # Detailed Health Information Display
        st.subheader(t['health_title'])
        info = CATEGORIES_INFO[lang][cat_key]

        col1, col2 = st.columns(2)
        with col1:
            st.warning(f"**{t['cat_lbl']}**\n\n{info['cat_name']}")
            st.info(f"**{t['status_lbl']}**\n\n{info['status']}")
            st.write(f"**{t['nutrients_lbl']}**\n{info['nutrients']}")
        
        with col2:
            st.write(f"**{t['effect_lbl']}**\n{info['health_effect']}")
            st.write(f"**{t['time_lbl']}**\n{info['best_time']}")
            st.write(f"**{t['buy_lbl']}**\n{info['purchase_time']}")
