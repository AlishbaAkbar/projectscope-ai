#!/usr/bin/env python
"""
Test script for Phase 6 (Feature Extraction) and Phase 7 (Task Decomposition)
Run this from terminal: python test_phase_6_7.py
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.feature_extractor import FeatureExtractor # type: ignore
from app.services.task_decomposer import TaskDecomposer
from app.models.feature import Feature
from app.models.task import Task

class MockRequirement:
    """Mock requirement for testing"""
    def __init__(self, text, id=1):
        self.text = text
        self.id = id

def test_feature_extraction():
    """Test Phase 6: Feature Extraction"""
    print("\n" + "=" * 70)
    print("🧪 TESTING PHASE 6: FEATURE EXTRACTION")
    print("=" * 70)
    
    # Test scenarios - different types of projects
    test_cases = [
        {
            "name": "E-commerce Store",
            "requirements": [
                MockRequirement("Users can login and register accounts"),
                MockRequirement("Browse products with search and filters"),
                MockRequirement("Add items to cart and checkout"),
                MockRequirement("Process payments via credit card"),
                MockRequirement("Track orders and order history"),
                MockRequirement("Admin panel to manage products and orders")
            ]
        },
        {
            "name": "Social Media App",
            "requirements": [
                MockRequirement("Users can create profiles and login"),
                MockRequirement("Post updates and share content"),
                MockRequirement("Follow other users and see their posts"),
                MockRequirement("Like and comment on posts"),
                MockRequirement("Real-time notifications")
            ]
        },
        {
            "name": "Simple Blog",
            "requirements": [
                MockRequirement("Authors can login and write posts"),
                MockRequirement("Posts have categories and tags"),
                MockRequirement("Readers can comment on posts"),
                MockRequirement("Search functionality for posts")
            ]
        }
    ]
    
    extractor = FeatureExtractor()
    all_results = []
    
    for test_case in test_cases:
        print(f"\n📋 Project: {test_case['name']}")
        print(f"   Requirements: {len(test_case['requirements'])}")
        
        try:
            features = extractor.extract_features(test_case['requirements'])
            
            print(f"   ✅ Extracted {len(features)} features:")
            for feature in features:
                print(f"      • {feature.canonical_name} (Priority: {feature.priority}, Complexity: {feature.complexity}/10)")
            
            all_results.append({
                "name": test_case['name'],
                "features": features,
                "status": "PASS"
            })
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            all_results.append({
                "name": test_case['name'],
                "features": [],
                "status": "FAIL",
                "error": str(e)
            })
    
    return all_results

def test_task_decomposition():
    """Test Phase 7: Task Decomposition"""
    print("\n" + "=" * 70)
    print("🧪 TESTING PHASE 7: TASK DECOMPOSITION")
    print("=" * 70)
    
    # Use features from previous test
    extractor = FeatureExtractor()
    test_requirements = [
        MockRequirement("Users can login and register"),
        MockRequirement("Product catalog with search"),
        MockRequirement("Shopping cart and checkout"),
        MockRequirement("Payment processing"),
        MockRequirement("Order tracking"),
        MockRequirement("Admin dashboard")
    ]
    
    print("\n📋 Test Project: Complete E-commerce")
    print(f"   Requirements: {len(test_requirements)}")
    
    try:
        features = extractor.extract_features(test_requirements)
        print(f"   ✅ Features extracted: {len(features)}")
        
        decomposer = TaskDecomposer()
        tasks = decomposer.decompose_features(features)
        
        print(f"   ✅ Tasks generated: {len(tasks)}")
        
        # Show summary by role
        from collections import defaultdict
        role_summary = defaultdict(lambda: {"count": 0, "total_hours": 0})
        
        for task in tasks:
            role_summary[task.role_id]["count"] += 1
            role_summary[task.role_id]["total_hours"] += task.estimated_hours
        
        print("\n   📊 Task Summary by Role:")
        for role_id, data in role_summary.items():
            print(f"      • Role {role_id}: {data['count']} tasks, {data['total_hours']} hours")
        
        # Show some sample tasks
        print("\n   📝 Sample Tasks:")
        for task in tasks[:5]:  # First 5 tasks
            print(f"      • {task.title}")
            print(f"        - Hours: {task.estimated_hours}h (Min: {task.min_hours}h, Max: {task.max_hours}h)")
            print(f"        - Priority: {task.priority}")
            print()
        
        return {
            "status": "PASS",
            "num_features": len(features),
            "num_tasks": len(tasks),
            "tasks": tasks
        }
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {
            "status": "FAIL",
            "error": str(e)
        }

def test_dependency_graph():
    """Test the dependency graph functionality"""
    print("\n" + "=" * 70)
    print("🧪 TESTING DEPENDENCY GRAPH")
    print("=" * 70)
    
    try:
        from app.estimation.task_dependencies import TaskDependencyGraph
        
        # Create sample tasks with dependencies
        sample_tasks = [
            {"id": "task1", "hours": 8, "dependencies": []},
            {"id": "task2", "hours": 12, "dependencies": ["task1"]},
            {"id": "task3", "hours": 6, "dependencies": ["task1"]},
            {"id": "task4", "hours": 10, "dependencies": ["task2", "task3"]},
            {"id": "task5", "hours": 4, "dependencies": ["task4"]},
        ]
        
        graph = TaskDependencyGraph(sample_tasks)
        
        print("\n   📋 Tasks with dependencies:")
        for task in sample_tasks:
            print(f"      • {task['id']}: {task['hours']}h, depends on: {task['dependencies']}")
        
        # Get critical path
        critical_path, total_hours = graph.get_critical_path()
        print(f"\n   🎯 Critical Path: {' → '.join(critical_path)}")
        print(f"   ⏱️  Total Hours: {total_hours}h")
        
        # Get parallelization opportunities
        parallel_opps = graph.get_parallelization_opportunities()
        print(f"\n   🔄 Parallelization Opportunities: {len(parallel_opps.get('parallelization_opportunities', []))}")
        
        # Get bottlenecks
        bottlenecks = graph.get_bottlenecks()
        print(f"\n   🚧 Bottlenecks Found: {len(bottlenecks)}")
        for bottleneck in bottlenecks:
            print(f"      • {bottleneck['task_id']}: {bottleneck['warning']}")
        
        return {
            "status": "PASS",
            "critical_path": critical_path,
            "total_hours": total_hours
        }
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {
            "status": "FAIL",
            "error": str(e)
        }

def main():
    """Main test function"""
    print("=" * 70)
    print("🚀 PROJECTSCOPE AI - PHASE 6 & 7 TEST SUITE")
    print("=" * 70)
    
    results = {
        "feature_extraction": test_feature_extraction(),
        "task_decomposition": test_task_decomposition(),
        "dependency_graph": test_dependency_graph()
    }
    
    # Print final summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results.items():
        if isinstance(result, list):  # Feature extraction has multiple test cases
            passed = sum(1 for r in result if r["status"] == "PASS")
            total = len(result)
            status = "✅ PASS" if passed == total else "⚠️ PARTIAL"
            print(f"   {test_name}: {status} ({passed}/{total})")
        else:
            status = "✅ PASS" if result.get("status") == "PASS" else "❌ FAIL"
            print(f"   {test_name}: {status}")
    
    print("\n" + "=" * 70)
    print("🎉 TESTING COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()