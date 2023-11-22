from todo_app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)



# def greet():
#     return f"Hello, shabzy!"

# def farewell(name):
#     return f"Goodbye, {name}!"

# # Pass function names as values directly
# # selected_function = greet
# result = greet

# print(result) 
