def is_email_registered(email):
    """Check if an email is already registered in the users table."""
    try:
        response = supabase.table("users").select("email").eq("email", email).execute()
        return len(response.data) > 0  # True if email exists
    except Exception as e:
        print("Error checking email:", e)
        return False  # Assume not registered if an error occurs

def store_user_email(email):
    """Store the registered email in the users table."""
    try:
        supabase.table("users").insert({"email": email}).execute()
        print("Email stored successfully!")
    except Exception as e:
        print("Error storing email:", e)

def signup():
    """Signup function with email verification."""
    email = input("Enter your email: ")
    password = input("Enter a password: ")
    confirm_password = input("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return
    if is_email_registered(email):
        print("This email is already registered. Try logging in instead.")
        return

    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        print("Signup successful! Check your email for verification.")

        # Store email in the `users` table
        store_user_email(email)  # ✅ Only calling this function once
    except Exception as e:
        print("Signup failed. Error:", e)

def login():
    try:
        stored_email = keyring.get_password("app", "email")
        stored_password = keyring.get_password("app", "password")
        
        if stored_email and stored_password:
            print("Auto-logging in...")
            email, password = stored_email, stored_password
        else:
            email = input("Enter your email: ")
            password = input("Enter your password: ")

        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        if response:
            user = supabase.auth.get_user()
            # Access the user data correctly through the user object
            if user and user.user.email_confirmed_at:  # Check if email is confirmed
                print("Login successful!")
                keyring.set_password("app", "email", email)
                keyring.set_password("app", "password", password)
                return True
            else:
                print("Please verify your email before logging in.")
        else:
            print("Invalid email or password.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def logout():
    try:
        confirmation = input("Are you sure you want to logout? (y/n): ").lower()
        if confirmation == 'y':
            keyring.delete_password("app", "email")
            keyring.delete_password("app", "password")
            print("Logged out successfully!")
        else:
            print("Logout cancelled.")
    except Exception as e:
        if str(e) == "app":
            print("No stored credentials found.")
        else:
            print(f"An error occurred: {str(e)}")

def main():
    while True:
        choice = input("\n1. Signup\n2. Login\n3. Logout\n4. Exit\nChoose an option: ")
        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            logout()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
