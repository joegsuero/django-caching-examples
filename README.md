---
## Experience Caching in Action!

I've shared the concepts and my experience with you, but nothing beats hands-on practice. I've created a GitHub repository with all the code examples we've discussed, ready for you to explore and, more importantly, test yourself.
---

### The Example and Benchmark Repository

The repository [`django-caching-Examples`](https://github.com/joegsuero/django-caching-examples) contains:

- **Caching Configuration:** Demonstrations of `LocMemCache`, `FileBasedCache`, `DatabaseCache`, and examples of how to configure `RedisCache` and `MemcachedCache`.
- **Per-View Caching:** Views decorated with `@cache_page` and a comparison view without caching so you can see the difference.
- **Template Fragment Caching:** A clear example of how to cache specific sections of your templates.
- **Low-Level Cache API:** Demonstrations of how to use `cache.get()` and `cache.set()` to optimize heavy calculations or ORM results.
- **Useful Antipattern: Caching External APIs:** A practical example of how to reduce reliance on slow external services using Django's caching system.

---

### How to Test and Benchmark

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/joegsuero/django-caching-examples.git](https://github.com/joegsuero/django-caching-examples.git)
    cd django-caching-examples
    ```
2.  **Set Up Your Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
3.  **Prepare the Database and Cache:**

    ```bash
    python manage.py migrate
    python manage.py createsuperuser # Optional, to access the admin
    python manage.py createcachetable my_cache_table # If you want to use DatabaseCache
    ```

    Visit `/admin` and add some **Categories** and **Products** to have data to work with in the examples.

4.  **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

    Open your browser and visit the different URLs under `/app/` to interact with the examples (e.g., `http://127.0.0.1:8000/app/products/cached/`). Observe your server console; it will indicate whether the content is served from the database or from the cache.

5.  **Perform Benchmarks with ApacheBench (`ab`):**
    `ab` is a command-line tool for testing web server performance. Install it if you don't have it (on Debian/Ubuntu: `sudo apt-get install apache2-utils`).

    - **No Cache (Baseline):**

      ```bash
      ab -n 100 -c 10 [http://127.0.0.1:8000/app/products/uncached/](http://127.0.0.1:8000/app/products/uncached/)
      ```

      Look at the `Requests per second`. This will be your starting point.

    - **With Per-View Caching:**
      First, "warm up" the cache (make a first request so the cache is generated):

      ```bash
      ab -n 1 -c 1 [http://127.0.0.1:8000/app/products/cached/](http://127.0.0.1:8000/app/products/cached/)
      ```

      Then, run the benchmark:

      ```bash
      ab -n 100 -c 10 [http://127.0.0.1:8000/app/products/cached/](http://127.0.0.1:8000/app/products/cached/)
      ```

      Compare the `Requests per second` with the no-cache example! The improvement should be significant.

    - **Test the other examples** (Low-Level API, External API, Site-Wide Cache) following a similar methodology: a first request to fill the cache, and then a benchmark under load. Remember to activate the cache middlewares in `settings.py` for Site-Wide Caching.

---

### Additional Conclusion

By interacting with these examples and running the benchmarks, you will see firsthand the transformative power of caching. It's not just about reducing server load, but about delivering a superior user experience, a critical aspect of any modern application.

I encourage you to clone the repository, play with the code, and see the magic of caching for yourself!

---
