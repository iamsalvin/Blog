import os
import django
import random
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post, Comment, Profile

def create_sample_content():
    # Ensure admin user exists
    try:
        admin_user = User.objects.get(username='admin')
        print("Admin user already exists")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Created admin user")
    
    # Create some sample users
    sample_users = []
    for i in range(1, 4):
        username = f'user{i}'
        try:
            user = User.objects.get(username=username)
            print(f"User {username} already exists")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=f'user{i}@example.com',
                password='password123',
                first_name=f'User {i}',
                last_name='Sample'
            )
            print(f"Created user {username}")
        
        # Update the user's profile or leave as is if it already exists
        try:
            profile = Profile.objects.get(user=user)
            # Optionally update the profile if needed
            if not profile.bio:
                profile.bio = f'This is a sample bio for {username}'
                profile.save()
                print(f"Updated profile for {username}")
        except Profile.DoesNotExist:
            # This shouldn't happen due to the signals, but just in case
            Profile.objects.create(user=user, bio=f'This is a sample bio for {username}')
            print(f"Created profile for {username}")
            
        sample_users.append(user)
    
    # Create some sample categories
    categories = [
        {'name': 'Technology', 'slug': 'technology'},
        {'name': 'Travel', 'slug': 'travel'},
        {'name': 'Food', 'slug': 'food'},
        {'name': 'Health', 'slug': 'health'},
        {'name': 'Science', 'slug': 'science'}
    ]
    
    category_objects = []
    for category_data in categories:
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            slug=category_data['slug']
        )
        if created:
            print(f"Created category {category.name}")
        else:
            print(f"Category {category.name} already exists")
        category_objects.append(category)
    
    # Create some sample posts
    sample_posts = [
        {
            'title': 'The Future of AI Technology',
            'content': """
                Artificial Intelligence (AI) is rapidly transforming our world in ways we could only imagine a decade ago. From virtual assistants like Siri and Alexa to advanced machine learning models that can diagnose diseases, AI is becoming increasingly integrated into our daily lives.

                ## Recent Advancements
                
                Recent breakthroughs in natural language processing have led to models that can understand and generate human-like text. These models are being used in a variety of applications, from customer service chatbots to content creation tools.
                
                ## Ethical Considerations
                
                As AI technology advances, we must also consider the ethical implications. Issues such as bias in AI algorithms, privacy concerns, and the potential impact on employment are important topics that require careful consideration.
                
                ## Future Directions
                
                The future of AI looks promising, with potential applications in areas such as autonomous vehicles, personalized medicine, and sustainable energy. However, responsible development and regulation will be key to ensuring that AI benefits humanity as a whole.
            """,
            'category': 'Technology'
        },
        {
            'title': 'Exploring the Hidden Gems of Southeast Asia',
            'content': """
                Southeast Asia is a treasure trove of natural beauty, rich culture, and unforgettable experiences. Beyond the well-known destinations like Bangkok and Bali, there are countless hidden gems waiting to be discovered.

                ## Vietnam's Coastal Paradise
                
                The coastal town of Hoi An in Vietnam offers a perfect blend of history, culture, and natural beauty. With its well-preserved Ancient Town, beautiful beaches, and delicious cuisine, Hoi An is a must-visit destination for any traveler to Southeast Asia.
                
                ## Cambodia Beyond Angkor Wat
                
                While Angkor Wat is undoubtedly Cambodia's most famous attraction, the country has much more to offer. The peaceful riverside town of Kampot, with its French colonial architecture and proximity to Bokor National Park, provides a refreshing escape from the crowds.
                
                ## The Philippines' Island Paradise
                
                The Philippines is home to some of the most beautiful islands in the world. Palawan, with its stunning limestone cliffs, crystal-clear lagoons, and rich marine life, offers an unspoiled paradise for nature lovers and adventure seekers.
            """,
            'category': 'Travel'
        },
        {
            'title': 'The Science Behind a Perfect Cup of Coffee',
            'content': """
                Coffee is more than just a morning ritual for millions of people around the world – it's a complex beverage with a rich history and a fascinating science behind it.

                ## The Bean
                
                The journey to a perfect cup begins with the coffee bean. Coffee beans are actually seeds from the fruit of the Coffea plant, typically either Arabica or Robusta. Factors such as soil, altitude, climate, and processing methods all influence the flavor profile of the beans.
                
                ## The Roast
                
                Roasting transforms the green coffee beans into the aromatic brown beans we're familiar with. The roasting process causes chemical changes as the beans are rapidly heated, developing their characteristic flavor. Light, medium, and dark roasts each offer different taste experiences.
                
                ## The Brew
                
                The brewing method can significantly impact the taste of your coffee. Variables such as water temperature, grind size, brewing time, and water-to-coffee ratio all play crucial roles. Popular methods include pour-over, French press, espresso, and cold brew, each extracting different compounds from the coffee grounds.
                
                ## The Chemistry
                
                Coffee contains over 1,000 aroma compounds and numerous acids, oils, and other substances that contribute to its flavor. Caffeine, while famous for its stimulating effects, actually contributes very little to the taste. Instead, compounds such as chlorogenic acids, trigonelline, and various sugars and lipids create coffee's complex flavor profile.
            """,
            'category': 'Food'
        },
        {
            'title': 'Mindfulness Meditation: A Path to Better Health',
            'content': """
                In our fast-paced, constantly connected world, the practice of mindfulness meditation offers a valuable opportunity to slow down, reconnect with ourselves, and improve our overall well-being.

                ## What is Mindfulness?
                
                Mindfulness is the practice of intentionally focusing on the present moment, while calmly acknowledging and accepting one's feelings, thoughts, and bodily sensations. It's about being fully present and engaged in whatever you're doing, free from distraction or judgment.
                
                ## The Health Benefits
                
                Research has shown that regular mindfulness practice can have numerous health benefits, including reduced stress, improved sleep, better emotional regulation, and even physical changes such as reduced blood pressure and strengthened immune function.
                
                ## Getting Started
                
                Beginning a mindfulness practice doesn't require any special equipment or extensive training. Simple exercises such as focusing on your breath, body scanning, or mindful walking can be effective ways to start incorporating mindfulness into your daily routine.
                
                ## Consistency is Key
                
                Like any skill, mindfulness improves with practice. Even just a few minutes of daily meditation can lead to significant benefits over time. The key is consistency and patience, allowing yourself to experience the practice without expectations or judgments.
            """,
            'category': 'Health'
        },
        {
            'title': 'The Fascinating World of Quantum Physics',
            'content': """
                Quantum physics, the study of matter and energy at the most fundamental level, challenges our intuition and reveals a universe far stranger than we could have imagined.

                ## The Quantum Revolution
                
                In the early 20th century, scientists discovered that the laws governing the everyday world of classical physics break down at the atomic and subatomic levels. This led to the development of quantum mechanics, a theory that has revolutionized our understanding of the physical world.
                
                ## Wave-Particle Duality
                
                One of the most mind-bending concepts in quantum physics is wave-particle duality. It suggests that all particles, including electrons and photons, can behave as both particles and waves. This duality is demonstrated in the famous double-slit experiment, where particles create an interference pattern typical of waves.
                
                ## Quantum Entanglement
                
                Einstein called it "spooky action at a distance" – quantum entanglement occurs when pairs or groups of particles interact in ways such that the quantum state of each particle cannot be described independently of the others, even when separated by large distances.
                
                ## Practical Applications
                
                Despite its abstract nature, quantum physics has led to numerous practical applications, including lasers, transistors, and MRI machines. Emerging technologies like quantum computing and quantum cryptography promise to revolutionize information processing and security in the coming decades.
            """,
            'category': 'Science'
        }
    ]
    
    posts_created = []
    for post_data in sample_posts:
        # Find the category
        category = next((c for c in category_objects if c.name == post_data['category']), None)
        if not category:
            continue
            
        # Create a unique slug
        base_slug = slugify(post_data['title'])
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Pick a random author
        author = random.choice([admin_user] + sample_users)
        
        # Create post with random date in the last month
        days_ago = random.randint(0, 30)
        created_date = timezone.now() - timedelta(days=days_ago)
        
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'slug': slug,
                'author': author,
                'content': post_data['content'],
                'created_on': created_date
            }
        )
        
        if created:
            # Add category
            post.categories.add(category)
            print(f"Created post '{post.title}' by {post.author.username}")
            posts_created.append(post)
            
            # Add some random likes
            for _ in range(random.randint(0, len(sample_users))):
                user = random.choice(sample_users)
                if user not in post.likes.all():
                    post.likes.add(user)
        else:
            print(f"Post '{post.title}' already exists")
            posts_created.append(post)
    
    # Create some comments
    if posts_created:
        sample_comments = [
            "Great post! Thanks for sharing this information.",
            "I found this really interesting. Looking forward to more content like this.",
            "This is exactly what I needed to know. Very helpful!",
            "I have a question about this topic. Can you elaborate more on the third point?",
            "I disagree with some points here, but overall a good read.",
            "Well written and informative!",
            "This changed my perspective on the subject.",
            "I'll be sharing this with my friends.",
            "I've been researching this topic for a while, and this is one of the best explanations I've found.",
            "The examples you provided really helped clarify the concept."
        ]
        
        for post in posts_created:
            # Add 1-5 comments per post if it doesn't have any yet
            if post.comments.count() == 0:
                for _ in range(random.randint(1, 5)):
                    # Pick a random author different from post author
                    available_users = [u for u in sample_users if u != post.author]
                    if not available_users:
                        available_users = sample_users
                        
                    author = random.choice(available_users)
                    content = random.choice(sample_comments)
                    
                    # Create comment with random date after post creation but before now
                    max_days = (timezone.now() - post.created_on).days
                    if max_days > 0:
                        days_after = random.randint(0, max_days)
                    else:
                        days_after = 0
                        
                    comment_date = post.created_on + timedelta(days=days_after)
                    
                    Comment.objects.create(
                        post=post,
                        author=author,
                        content=content,
                        created_on=comment_date
                    )
                    print(f"Added comment to '{post.title}' by {author.username}")
    
    print("\nSample content creation complete!")
    print("You can login with the following accounts:")
    print("Admin: username='admin', password='admin123'")
    for i in range(1, 4):
        print(f"User {i}: username='user{i}', password='password123'")

if __name__ == "__main__":
    create_sample_content()
