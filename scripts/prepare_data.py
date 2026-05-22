import json
import random

system_prompt = (
    "당신은 개발 개념을 설명하는 AI 튜터입니다. "
    "개발 관련 질문에는 정의, 내부 동작, 장단점, 사용 상황을 중심으로 설명하세요. "
    "일반 질문에는 자연스럽고 간결하게 답변하세요."
)

categories = {
    "List": {
        "questions": [
            "C#의 List<T>가 뭐야?",
            "List와 Array 차이 설명해줘",
            "List<T> 내부 구조 설명해줘",
            "왜 List는 동적 배열이라고 불려?",
            "게임 개발에서 List를 많이 쓰는 이유는?"
        ],
        "answers": [
            "List<T>는 C#에서 제공하는 제네릭 컬렉션으로 내부적으로 동적 배열 기반으로 구현됩니다. 배열보다 유연하게 크기를 늘릴 수 있으며 인덱스 접근 속도가 빠릅니다. 다만 중간 삽입이나 삭제 시 요소 이동 비용이 발생할 수 있습니다. 실무에서는 순차 데이터 관리나 게임 오브젝트 목록 관리 등에 자주 사용됩니다.",
            "Array는 크기가 고정된 자료구조이고 List<T>는 크기를 동적으로 변경할 수 있는 컬렉션입니다. List<T>는 내부 배열의 Capacity를 자동으로 늘리며 데이터를 관리합니다. 따라서 사용 편의성은 높지만 Capacity 증가 시 메모리 재할당이 발생할 수 있습니다.",
            "List<T>는 내부적으로 배열을 사용합니다. 데이터가 Capacity를 초과하면 더 큰 배열을 새로 생성한 뒤 기존 데이터를 복사합니다. 인덱스 접근은 빠르지만 중간 삽입과 삭제는 상대적으로 비용이 큽니다.",
            "List<T>는 내부 배열 크기를 자동으로 확장하기 때문에 동적 배열이라고 불립니다. 데이터가 증가하면 새로운 큰 배열을 생성하고 기존 데이터를 복사합니다.",
            "게임 개발에서는 오브젝트 목록이나 적 리스트처럼 개수가 자주 변하는 데이터를 관리해야 하는 경우가 많습니다. 이런 상황에서 List<T>는 사용이 편리하고 인덱스 접근이 빨라 자주 사용됩니다."
        ]
    },

    "Dictionary": {
        "questions": [
            "Dictionary<TKey, TValue>가 뭐야?",
            "Dictionary와 List 차이 설명해줘",
            "Dictionary 내부 구조 설명해줘",
            "왜 Dictionary 조회 속도가 빠른거야?",
            "Dictionary 사용 시 주의할 점은?"
        ],
        "answers": [
            "Dictionary<TKey, TValue>는 key-value 형태로 데이터를 저장하는 해시 기반 컬렉션입니다. 키를 통해 빠르게 데이터를 조회할 수 있습니다. 다만 해시 충돌 관리와 키 동등성 비교가 중요합니다.",
            "List는 순차 데이터를 관리하는 데 적합하고 Dictionary는 키 기반 빠른 검색에 적합합니다. List는 인덱스를 사용하고 Dictionary는 key를 사용합니다.",
            "Dictionary는 내부적으로 해시 테이블 구조를 사용합니다. key의 hash 값을 기반으로 저장 위치를 계산하여 빠른 검색을 수행합니다.",
            "Dictionary는 key를 hash 값으로 변환해 바로 위치를 찾기 때문에 평균적으로 O(1)에 가까운 조회 성능을 가집니다.",
            "Dictionary는 중복 key를 허용하지 않습니다. 또한 mutable 객체를 key로 사용하는 경우 hash 값 변경 문제가 발생할 수 있어 주의해야 합니다."
        ]
    },

    "Stack": {
        "questions": [
            "Stack이 뭐야?",
            "Stack과 Queue 차이 설명해줘",
            "Stack은 왜 LIFO 구조야?",
            "게임 개발에서 Stack 사용 예시는?",
            "Stack의 대표 연산은 뭐야?"
        ],
        "answers": [
            "Stack은 가장 마지막에 들어간 데이터가 가장 먼저 나오는 LIFO 구조의 자료구조입니다. Push와 Pop 연산을 사용합니다.",
            "Stack은 마지막에 들어간 데이터를 먼저 꺼내고 Queue는 먼저 들어간 데이터를 먼저 꺼냅니다. Stack은 LIFO, Queue는 FIFO 구조입니다.",
            "Stack은 가장 위(top) 데이터만 접근하기 때문에 마지막에 들어간 데이터가 먼저 제거됩니다. 그래서 LIFO 구조라고 부릅니다.",
            "게임 개발에서는 상태 복구, Undo 기능, UI 이전 화면 관리 등에 Stack이 자주 사용됩니다.",
            "Stack의 대표 연산은 Push, Pop, Peek입니다. Push는 데이터 삽입, Pop은 제거, Peek는 최상단 데이터 확인입니다."
        ]
    },

    "Queue": {
        "questions": [
            "Queue가 뭐야?",
            "Queue와 Stack 차이 설명해줘",
            "Queue는 어디에 사용돼?",
            "Queue 내부 동작 설명해줘",
            "왜 BFS에서 Queue를 사용할까?"
        ],
        "answers": [
            "Queue는 먼저 들어온 데이터가 먼저 나가는 FIFO 구조의 자료구조입니다. Enqueue와 Dequeue 연산을 사용합니다.",
            "Queue는 먼저 들어온 데이터를 먼저 처리하고 Stack은 마지막 데이터를 먼저 처리합니다.",
            "Queue는 작업 대기열, 이벤트 처리, BFS 탐색 등에 자주 사용됩니다.",
            "Queue는 일반적으로 배열 기반 순환 버퍼나 연결 리스트 방식으로 구현됩니다.",
            "BFS는 먼저 방문한 노드를 먼저 탐색해야 하므로 FIFO 구조인 Queue가 적합합니다."
        ]
    },

    "OOP": {
        "questions": [
            "객체지향 프로그래밍이 뭐야?",
            "상속이 뭐야?",
            "캡슐화 설명해줘",
            "다형성이 뭐야?",
            "인터페이스를 사용하는 이유는?"
        ],
        "answers": [
            "객체지향 프로그래밍은 데이터를 객체 단위로 관리하고 객체 간 상호작용을 중심으로 개발하는 방식입니다.",
            "상속은 기존 클래스의 기능을 재사용하고 확장할 수 있게 해주는 객체지향 개념입니다.",
            "캡슐화는 데이터를 외부에서 직접 접근하지 못하게 하고 메서드를 통해 제어하는 개념입니다.",
            "다형성은 같은 인터페이스나 메서드 호출이 상황에 따라 다르게 동작하는 특성입니다.",
            "인터페이스는 객체 간 결합도를 낮추고 유연한 구조를 만들기 위해 사용됩니다."
        ]
    },

    "General": {
        "questions": [
            "한국의 수도는 어디야?",
            "AI가 뭐야?",
            "오늘 날씨 어때?",
            "프로그래밍은 왜 배우는거야?",
            "게임 개발은 어려워?"
        ],
        "answers": [
            "대한민국의 수도는 서울입니다.",
            "AI는 인간의 학습과 판단 능력을 컴퓨터로 구현하려는 기술입니다.",
            "실시간 날씨는 기상 서비스를 통해 확인하는 것이 가장 정확합니다.",
            "프로그래밍은 문제를 논리적으로 해결하고 다양한 소프트웨어를 만들기 위해 배웁니다.",
            "게임 개발은 그래픽, 로직, 네트워크 등 다양한 기술이 필요해 어렵지만 그만큼 재미있는 분야입니다."
        ]
    }
}


def generate_dataset(target_count=1000):
    dataset = []

    category_names = list(categories.keys())

    while len(dataset) < target_count:
        category = random.choice(category_names)

        q = random.choice(categories[category]["questions"])
        a = random.choice(categories[category]["answers"])

        item = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": q
                },
                {
                    "role": "assistant",
                    "content": a
                }
            ]
        }

        dataset.append(item)

    return dataset


def save_jsonl(dataset, filename="csharp_dev_concept_dataset_1000.jsonl"):
    with open(filename, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    dataset = generate_dataset(1000)
    save_jsonl(dataset)

    print(f"생성 완료: {len(dataset)}개")
    print("파일명: csharp_dev_concept_dataset_1000.jsonl")
