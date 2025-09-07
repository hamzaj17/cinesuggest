from hybrid import hybrid_recommend

if __name__ == "__main__":
    movie_name = "Interstellar"
    recommendations = hybrid_recommend(movie_name, user_id=1, top_n=5, weight_cb=0.6, weight_cf=0.4)  
    print(f"Hybrid recommendations for '{movie_name}':")
    for idx, rec in enumerate(recommendations, start=1):
        print(f"{idx}. {rec}")


# To run this script, use the command:
#python -m src.main  