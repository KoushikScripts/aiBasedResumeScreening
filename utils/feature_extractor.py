# utils/feature_extractor.py

def extract_features(text):
    text = text.lower()
    return {
        'length': len(text),
        'word_count': len(text.split()),
        'num_skills': text.count('skill'),
        'num_projects': text.count('project'),
        'num_certifications': text.count('certification'),
        'has_summary': int('summary' in text),
        'has_experience': int('experience' in text),
        'has_education': int('education' in text),
        'has_awards': int('award' in text or 'achievement' in text),
        'num_action_words': sum(text.count(word) for word in ['led', 'developed', 'managed', 'spearheaded']),
    }

