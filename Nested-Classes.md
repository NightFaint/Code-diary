  # 嵌套类概述
  Java允许在一个类中定义另一个类，这样的类称为嵌套类。
	
	class OuterClass
	{
	    ...
	    class NestedClass
	    {
	        ...
	    }
	}
	
  嵌套类根据声明时是静态(static)还是非静态(non-static)的又分为两个类型：static nested classes和inner class(non-static
  classes)(内部类)。
  
	class OuterClass
	{
		...
		static class StaticNestedClass
		{
			...
		}
		class InnerClass
		{
			...
		}
	}
	
  嵌套类是外部类的一个成员。内部类对外部类的实例域(可以理解为python中实例的属性)有访问权限，即使这些实例域被定义为
私有的(private)。但是，静态的嵌套类(static nested classes)对外部类的实例域是没有访问权限的。嵌套类可被声明为private,
public，protected。

  使用嵌套类的原因有以下几点：
  
  - 逻辑上，如果一个类只在一个地方使用，那么倾向于把这个类嵌套在我们要用的地方，即另一个类中。
  - 增加了封装性：考虑两个类A和B，如果B需要访问A中被声明为private的实例域，那么把B嵌套在A中可以实现该目的，而不用把A
  的实例域声明为public破坏封装性。另一方面，B嵌套在A中，也使得只有A才能访问B，与外界隔离开来。
  - 增加代码可读性和可维护性。
  
  **Static Nested Classes**
  
  静态的嵌套类通过外部类的类名访问：OuterClass.StaticNestedClass。
  
  例如，创建一个·静态嵌套类对象：
  
	OuterClass.StaticNestedClass nestedObject=new OuterClass.StaticNestedClass();

  **Inner Class**
  
  与实例方法和实例域一样，内部类与一个外部类的实例相关并且对实例方法和实例域有访问权限。注意，由于内部类属于外部类
  的一个实例对象，所以内部类不能定义静态变量。
  
  要创建一个内部类实例，必须有一个外部类实例。例如：
  
	OuterClass.InnerClass innerObject=outerObject.new InnerClass();
  
  内部类有以下几个优点：
  - 内部类方法可以访问外部类的数据，包括私有数据。
  - 内部类可以对同一个包中的其他类隐藏起来（嵌套类的优点）。
  - 当想要定义一个回调函数且不想编写大量代码时，可使用匿名内部类比较便捷。
  
  内部类有两个特殊的类型：局部类local classes和匿名类anonymous classes。
  
  **覆盖**
  
  如果在内部类声明一个变量或者参数，而这个变量或参数与闭包中(外部类)中的变量同名，那么会覆盖闭包中的变量，
  便无法通过单独的变量名引用闭包(外部类)中的变量。比如：
  	
	public class ShadowTest
	{
		public int x=0;
		class FirstLevel
		{
			public int x=1;
			void methodInFirstLevel(int x)
			{
				System.out.println("x= "+x);
				System.out.println("this.x= "+this.x);
				System.out.println("ShadowTest.this.x= "+ShadowTest.this.x);
			}
		}
		
		public static void main(String... args)
		{
			ShowdowTest st=new ShadowTest();
			ShowdowTest.FirstLevel f1=st.new FirstLevel();
			f1.methodInFirstLevel(23);
		}
	}
	
  输出如下：
  
	x=23
	this.x=1
	ShowdowTest.this.x=0
	
  
  优先级：方法methodInFirstLevel中的参数x > 内部类FirstLevel中的实例域x > 外部类ShowdowTest的实例域x。
  
参考：

  https://docs.oracle.com/javase/tutorial/java/javaOO/nested.html
  
  《java核心技术 卷1》
