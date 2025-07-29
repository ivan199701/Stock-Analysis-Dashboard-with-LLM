PIL.UnidentifiedImageError: cannot identify image file <_io.BytesIO object at 0x7fabcd9e32c0>
Traceback:
File "/app/src/presentation/ui/pages/main.py", line 46, in <module>
    main()
File "/app/src/presentation/ui/pages/main.py", line 41, in main
    render_dashboard()
File "/app/src/presentation/ui/pages/dashboard.py", line 80, in render_dashboard
    st.image("src/presentation/ui/assets/alpaca.jpg", caption="You found the secret alpaca!")
File "/usr/local/lib/python3.9/site-packages/streamlit/runtime/metrics_util.py", line 443, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/usr/local/lib/python3.9/site-packages/streamlit/elements/image.py", line 180, in image
    marshall_images(
File "/usr/local/lib/python3.9/site-packages/streamlit/elements/lib/image_utils.py", line 439, in marshall_images
    proto_img.url = image_to_url(
File "/usr/local/lib/python3.9/site-packages/streamlit/elements/lib/image_utils.py", line 329, in image_to_url
    image_format = _validate_image_format_string(image_data, output_format)
File "/usr/local/lib/python3.9/site-packages/streamlit/elements/lib/image_utils.py", line 112, in _validate_image_format_string
    pil_image = Image.open(io.BytesIO(image_data))
File "/usr/local/lib/python3.9/site-packages/PIL/Image.py", line 3580, in open
    raise UnidentifiedImageError(msg)