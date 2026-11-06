#!/usr/bin/env python3
"""Interactive birthday console workflow. Python 3.8+, standard library only.

Run: python birthday_gen.py
Quick run: python birthday_gen.py --name "نور" --no-delay --no-color
Messages are assembled locally from randomized phrases, not an AI service.
"""

import argparse
import os
import random
import sys
import time

RNG = random.SystemRandom()
OPENINGS = (
    "كل سنة وإنت طيب يا {name}!",
    "النهارده يومك يا {name}، والدنيا كلها بتحتفل بيك!",
    "عيد ميلاد سعيد يا {name}، يا صاحب أحلى ضحكة!",
    "يا {name}، سنة جديدة وحكاية حلوة بتبدأ!",
    "أحلى تهنئة لأحلى حد: {name}!",
)
WISHES = (
    "أتمنى لك سنة مليانة ضحك وراحة بال.",
    "يا رب أحلامك تقرب وخطواتك تنجح.",
    "أتمنى أيامك تبقى أخف وأجمل من كل اللي فات.",
    "يا رب تلاقي الفرحة في تفاصيل يومك الصغيرة.",
    "أتمنى لك مغامرات جديدة وذكريات تستاهل تتحكي.",
    "يا رب تكون دايمًا وسط ناس بتحبك وتقدرك.",
    "أتمنى لك صحة وحب ونجاح على قد قلبك الحلو.",
    "يا رب كل باب خير تتمناه يتفتح لك.",
)
CLOSINGS = (
    "اطفي الشمع واتمنى أمنية كبيرة!",
    "الكيكة مستنياك، والاحتفال لسه بيبدأ!",
    "خلي ابتسامتك عنوان السنة الجديدة!",
    "النهارده الفرح باسمك، وبكرة أجمل!",
    "دي بداية فصل جديد مليان حاجات حلوة!",
)
SYMBOLS = ("🎉", "🎊", "✨", "🎈", "🌟", "🎂", "🎁", "💛")


def generate_message(name, previous=None):
    """Include name and avoid an identical message on consecutive rerolls."""
    for _ in range(100):
        wishes = RNG.sample(WISHES, 2)
        message = "\n".join((
            RNG.choice(OPENINGS).format(name=name),
            *wishes,
            RNG.choice(CLOSINGS),
        ))
        if message != previous:
            return message
    # A deterministic fallback ensures consecutive results always differ.
    return message + "\nوخلي السنة دي بداية حلم جديد!"


def generate_confetti(previous=None):
    result = " ".join(RNG.choices(SYMBOLS, k=12))
    if result == previous:
        first = result.split(" ")[0]
        result = next(s for s in SYMBOLS if s != first) + result[len(first):]
    return result


def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        return None


def paint(text, color, enabled):
    return "\033[" + color + "m" + text + "\033[0m" if enabled else text


def celebrate(name, last_message, last_confetti, delay, color):
    print("\n" + "═" * 48)
    print(paint("🎂  BIRTHDAY WORKFLOW  🎂", "1;35", color))
    for step in ("[1/3] تجهيز الاسم: " + name,
                 "[2/3] خلط الأمنيات والتهاني...",
                 "[3/3] إطلاق الاحتفال!"):
        print(step, flush=True)
        if delay:
            time.sleep(0.2)
    message = generate_message(name, last_message)
    confetti = generate_confetti(last_confetti)
    print(paint(confetti, "1;33", color))
    print(paint(message, "1;36", color))
    print(confetti)
    print("═" * 48)
    return message, confetti


def main(argv=None):
    parser = argparse.ArgumentParser(description="مولد تهاني عيد ميلاد تفاعلي")
    parser.add_argument("--name", help="اسم صاحب عيد الميلاد؛ تشغيل واحد بدون أسئلة")
    parser.add_argument("--no-delay", action="store_true", help="إلغاء انتظار الأنيميشن")
    parser.add_argument("--no-color", action="store_true", help="إلغاء ألوان ANSI")
    args = parser.parse_args(argv)
    color = (sys.stdout.isatty() and not args.no_color
             and "NO_COLOR" not in os.environ and os.environ.get("TERM") != "dumb")
    name = args.name
    if name is not None:
        name = name.strip()
        if not name:
            parser.error("الاسم ما ينفعش يكون فاضي")
    else:
        print("🎁 أهلاً بيك في ورشة تهاني عيد الميلاد!")
        while True:
            name = safe_input("اكتب اسم صاحب عيد الميلاد: ")
            if name is None:
                print("\nمفيش إدخال؛ إلى اللقاء 👋")
                return 0
            name = name.strip()
            if name:
                break
            print("الاسم فاضي؛ اكتب اسم علشان نبدأ.")
    previous_message = previous_confetti = None
    while True:
        previous_message, previous_confetti = celebrate(
            name, previous_message, previous_confetti, not args.no_delay, color)
        if args.name is not None:
            return 0
        while True:
            choice = safe_input("\n[1] تهنئة جديدة  [2] تغيير الاسم  [0] خروج: ")
            if choice is None or choice.strip() in ("0", "٠"):
                print("مع السلامة، وخلي الفرحة مكملة! 👋")
                return 0
            choice = choice.strip()
            if choice in ("1", "١"):
                break
            if choice in ("2", "٢"):
                new_name = safe_input("اكتب الاسم الجديد: ")
                if new_name is None:
                    print("\nإلى اللقاء 👋")
                    return 0
                if not new_name.strip():
                    print("الاسم فاضي؛ الاسم الحالي زي ما هو.")
                    continue
                name = new_name.strip()
                break
            print("اختيار مش معروف؛ استخدم 1 أو 2 أو 0.")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nتم إيقاف الاحتفال بهدوء. إلى اللقاء 👋")
        sys.exit(0)
